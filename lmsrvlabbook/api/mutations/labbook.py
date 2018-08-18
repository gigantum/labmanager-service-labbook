# Copyright (c) 2018 FlashX, LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import base64
import os
from docker.errors import ImageNotFound
import shutil

import graphene

from lmcommon.configuration import Configuration, get_docker_client
from lmcommon.container.container import ContainerOperations
from lmcommon.dispatcher import (Dispatcher, jobs)
from lmcommon.labbook import LabBook, loaders
from lmcommon.logging import LMLogger
from lmcommon.files import FileOperations
from lmcommon.imagebuilder import ImageBuilder
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityRecord, ActivityType
from lmcommon.gitlib.gitlab import GitLabManager
from lmcommon.environment import ComponentManager

from lmsrvcore.api.mutations import ChunkUploadMutation, ChunkUploadInput
from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author
from lmsrvcore.auth.identity import parse_token

from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFavoriteConnection
from lmsrvlabbook.api.connections.labbookfileconnection import LabbookFileConnection
from lmsrvlabbook.api.connections.labbook import LabbookConnection
from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.labbookfile import LabbookFavorite, LabbookFile
from lmsrvlabbook.dataloader.labbook import LabBookLoader


logger = LMLogger.get_logger()


class CreateLabbook(graphene.relay.ClientIDMutation):
    """Mutation for creation of a new Labbook on disk"""

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        repository = graphene.String(required=True)
        component_id = graphene.String(required=True)
        revision = graphene.Int(required=True)
        is_untracked = graphene.Boolean(required=False)

    # Return the LabBook instance
    labbook = graphene.Field(lambda: Labbook)

    @classmethod
    def mutate_and_get_payload(cls, root, info, name, description, repository, component_id, revision,
                               is_untracked=False, client_mutation_id=None):
        username = get_logged_in_username()

        # Create a new empty LabBook
        lb = LabBook(author=get_logged_in_author())
        # TODO: Set owner/namespace properly once supported fully
        lb.new(owner={"username": username},
               username=username,
               name=name,
               description=description,
               bypass_lfs=is_untracked)

        if is_untracked:
            FileOperations.set_untracked(lb, 'input')
            FileOperations.set_untracked(lb, 'output')
            input_set = FileOperations.is_set_untracked(lb, 'input')
            output_set = FileOperations.is_set_untracked(lb, 'output')
            if not (input_set and output_set):
                raise ValueError(f'{str(lb)} untracking for input/output in malformed state')
            if not lb.is_repo_clean:
                raise ValueError(f'{str(lb)} should have clean Git state after setting for untracked')

        # Create a Activity Store instance
        store = ActivityStore(lb)

        # Create detail record
        adr = ActivityDetailRecord(ActivityDetailType.LABBOOK, show=False, importance=0)
        adr.add_value('text/plain', f"Created new LabBook: {username}/{name}")

        # Create activity record
        ar = ActivityRecord(ActivityType.LABBOOK,
                            message=f"Created new LabBook: {username}/{name}",
                            show=True,
                            importance=255,
                            linked_commit=lb.git.commit_hash)
        ar.add_detail_object(adr)

        # Store
        store.create_activity_record(ar)

        # Add Base component
        cm = ComponentManager(lb)
        cm.add_component("base", repository, component_id, revision)

        # Prime dataloader with labbook you just created
        dataloader = LabBookLoader()
        dataloader.prime(f"{username}&{username}&{lb.name}", lb)

        # Get a graphene instance of the newly created LabBook
        return CreateLabbook(labbook=Labbook(owner=username, name=lb.name))


class DeleteLabbook(graphene.ClientIDMutation):
    """Delete a labbook from disk. """
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        confirm = graphene.Boolean(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, confirm, client_mutation_id=None):
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, owner, 'labbooks',
                                             labbook_name)
        lb = LabBook(author=get_logged_in_author())
        lb.from_directory(inferred_lb_directory)

        if confirm:
            logger.warning(f"Deleting {str(lb)}...")
            try:
                lb, stopped = ContainerOperations.stop_container(labbook=lb, username=username)
            except OSError:
                pass
            lb, docker_removed = ContainerOperations.delete_image(labbook=lb, username=username)
            if not docker_removed:
                raise ValueError(f'Cannot delete docker image for {str(lb)} - unable to delete LB from disk')
            shutil.rmtree(lb.root_dir, ignore_errors=True)
            if os.path.exists(lb.root_dir):
                logger.error(f'Deleted {str(lb)} but root directory {lb.root_dir} still exists!')
                return DeleteLabbook(success=False)
            else:
                return DeleteLabbook(success=True)
        else:
            logger.info(f"Dry run in deleting {str(lb)} -- not deleted.")
            return DeleteLabbook(success=False)


class DeleteRemoteLabbook(graphene.ClientIDMutation):
    """Delete a labbook from the remote repository."""
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        confirm = graphene.Boolean(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, confirm, client_mutation_id=None):
        if confirm is True:
            # Load config data
            configuration = Configuration().config

            # Extract valid Bearer token
            token = None
            if hasattr(info.context.headers, 'environ'):
                if "HTTP_AUTHORIZATION" in info.context.headers.environ:
                    token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])
            if not token:
                raise ValueError("Authorization header not provided. Cannot perform remote delete operation.")

            # Get remote server configuration
            default_remote = configuration['git']['default_remote']
            admin_service = None
            for remote in configuration['git']['remotes']:
                if default_remote == remote:
                    admin_service = configuration['git']['remotes'][remote]['admin_service']
                    break

            if not admin_service:
                raise ValueError('admin_service could not be found')

            # Perform delete operation
            mgr = GitLabManager(default_remote, admin_service, access_token=token)
            mgr.remove_labbook(owner, labbook_name)
            logger.info(f"Deleted {owner}/{labbook_name} from the remote repository {default_remote}")

            # Remove locally any references to that cloud repo that's just been deleted.
            try:
                lb = LabBook()
                lb.from_name(get_logged_in_username(), owner, labbook_name)
                lb.remove_remote()
                lb.remove_lfs_remotes()
            except ValueError as e:
                logger.warning(e)

            return DeleteLabbook(success=True)
        else:
            logger.info(f"Dry run deleting {labbook_name} from remote repository -- not deleted.")
            return DeleteLabbook(success=False)


class ExportLabbook(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    job_key = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, client_mutation_id=None):

        username = get_logged_in_username()
        logger.info(f'Exporting LabBook: {username}/{owner}/{labbook_name}')

        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, owner, 'labbooks',
                                             labbook_name)
        lb = LabBook(author=get_logged_in_author())
        lb.from_directory(inferred_lb_directory)

        job_metadata = {'method': 'export_labbook_as_zip',
                        'labbook': lb.key}
        job_kwargs = {'labbook_path': lb.root_dir,
                      'lb_export_directory': os.path.join(working_directory, 'export')}
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.export_labbook_as_zip, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Exporting LabBook {lb.root_dir} in background job with key {job_key.key_str}")

        return ExportLabbook(job_key=job_key.key_str)


class ImportLabbook(graphene.relay.ClientIDMutation, ChunkUploadMutation):
    class Input:
        chunk_upload_params = ChunkUploadInput(required=True)

    import_job_key = graphene.String()
    build_image_job_key = graphene.String()

    @classmethod
    def mutate_and_wait_for_chunks(cls, info, **kwargs):
        return ImportLabbook()

    @classmethod
    def mutate_and_process_upload(cls, info, **kwargs):
        if not cls.upload_file_path:
            logger.error('No file uploaded')
            raise ValueError('No file uploaded')

        username = get_logged_in_username()
        logger.info(
            f"Handling ImportLabbook mutation: user={username},"
            f"owner={username}. Uploaded file {cls.upload_file_path}")

        job_metadata = {'method': 'import_labbook_from_zip'}
        job_kwargs = {
            'archive_path': cls.upload_file_path,
            'username': username,
            'owner': username,
            'base_filename': cls.filename
        }
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.import_labboook_from_zip, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Importing LabBook {cls.upload_file_path} in background job with key {job_key.key_str}")

        assumed_lb_name = cls.filename.replace('.lbk', '').split('_')[0]
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, username, 'labbooks',
                                             assumed_lb_name)
        build_img_kwargs = {
            'path': inferred_lb_directory,
            'username': username,
            'nocache': True
        }
        build_img_metadata = {
            'method': 'build_image',
            # TODO - we need labbook key but labbook is not available...
            'labbook': f"{username}|{username}|{assumed_lb_name}"
        }
        logger.warning(f"Using assumed labbook name {build_img_metadata['labbook']}, better solution needed.")
        build_image_job_key = dispatcher.dispatch_task(jobs.build_labbook_image, kwargs=build_img_kwargs,
                                                       dependent_job=job_key, metadata=build_img_metadata)
        logger.info(f"Adding dependent job {build_image_job_key} to build "
                    f"Docker image for labbook `{inferred_lb_directory}`")

        return ImportLabbook(import_job_key=job_key.key_str, build_image_job_key=build_image_job_key.key_str)


class ImportRemoteLabbook(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        remote_url = graphene.String(required=True)

    new_labbook_edge = graphene.Field(LabbookConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, remote_url, client_mutation_id=None):
        username = get_logged_in_username()
        logger.info(f"Importing remote labbook from {remote_url}")
        lb = LabBook(author=get_logged_in_author())
        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        # Extract valid Bearer token
        if hasattr(info.context, 'headers') and "HTTP_AUTHORIZATION" in info.context.headers.environ:
            token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        mgr = GitLabManager(default_remote, admin_service, token)
        mgr.configure_git_credentials(default_remote, username)
        try:
            collaborators = [collab[1] for collab in mgr.get_collaborators(owner, labbook_name) or []]
            is_collab = any([username == c for c in collaborators])
        except:
            is_collab = username == owner

        # IF user is collaborator, then clone in order to support collaboration
        # ELSE, this means we are cloning a public repo and can't push back
        #       so we change to owner to the given user so they can (re)publish
        #       and do whatever with it.
        make_owner = not is_collab
        logger.info(f"Getting from remote, make_owner = {make_owner}")
        lb = loaders.from_remote(remote_url, username, owner, labbook_name, labbook=lb,
                                 make_owner=make_owner)

        # TODO: Fix cursor implementation, this currently doesn't make sense
        cursor = base64.b64encode(f"{0}".encode('utf-8'))
        lbedge = LabbookConnection.Edge(node=Labbook(owner=lb.owner['username'], name=labbook_name),
                                        cursor=cursor)
        return ImportRemoteLabbook(new_labbook_edge=lbedge)
