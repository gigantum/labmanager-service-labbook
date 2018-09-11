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
import os
import base64
import graphene

from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook
from lmcommon.dispatcher import Dispatcher, jobs
from lmcommon.logging import LMLogger
from lmcommon.gitlib.gitlab import GitLabManager

from lmsrvcore.api import logged_mutation
from lmsrvcore.auth.identity import parse_token
from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author
from lmsrvlabbook.api.connections.labbook import LabbookConnection
from lmsrvlabbook.api.objects.labbook import Labbook as LabbookObject

logger = LMLogger.get_logger()


class PublishLabbook(graphene.relay.ClientIDMutation):

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        set_public = graphene.Boolean(required=False)

    job_key = graphene.String()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, set_public=False,
                               client_mutation_id=None):
        # Load LabBook
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, owner, 'labbooks', labbook_name)
        lb = LabBook(author=get_logged_in_author())
        lb.from_directory(inferred_lb_directory)

        # Extract valid Bearer token
        if "HTTP_AUTHORIZATION" in info.context.headers.environ:
            token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])
        else:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        job_metadata = {'method': 'publish_labbook',
                        'labbook': lb.key}
        job_kwargs = {'labbook_path': lb.root_dir,
                      'username': username,
                      'access_token': token,
                      'public': set_public}
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.publish_labbook, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Publishing LabBook {lb.root_dir} in background job with key {job_key.key_str}")

        return PublishLabbook(job_key=job_key.key_str)


class SyncLabbook(graphene.relay.ClientIDMutation):

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        force = graphene.Boolean(required=False)

    job_key = graphene.String()

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, force=False, client_mutation_id=None):
        # Load LabBook
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, owner, 'labbooks',
                                             labbook_name)
        lb = LabBook(author=get_logged_in_author())
        lb.from_directory(inferred_lb_directory)

        # Extract valid Bearer token
        token = None
        if hasattr(info.context.headers, 'environ'):
            if "HTTP_AUTHORIZATION" in info.context.headers.environ:
                token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])

        if not token:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        if not admin_service:
            raise ValueError('admin_service could not be found')

        # Configure git creds
        mgr = GitLabManager(default_remote, admin_service, access_token=token)
        mgr.configure_git_credentials(default_remote, username)

        job_metadata = {'method': 'sync_labbook',
                        'labbook': lb.key}
        job_kwargs = {'labbook_path': lb.root_dir,
                      'username': username,
                      'force': force}
        dispatcher = Dispatcher()
        job_key = dispatcher.dispatch_task(jobs.sync_labbook, kwargs=job_kwargs, metadata=job_metadata)
        logger.info(f"Syncing LabBook {lb.root_dir} in background job with key {job_key.key_str}")

        return SyncLabbook(job_key=job_key.key_str)


class SetVisibility(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        visibility = graphene.String(required=True)

    new_labbook_edge = graphene.Field(LabbookConnection.Edge)

    @classmethod
    @logged_mutation
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, visibility,
                               client_mutation_id=None):
        # Load LabBook
        username = get_logged_in_username()
        working_directory = Configuration().config['git']['working_directory']
        inferred_lb_directory = os.path.join(working_directory, username, owner, 'labbooks',
                                             labbook_name)
        lb = LabBook(author=get_logged_in_author())
        lb.from_directory(inferred_lb_directory)

        # Extract valid Bearer token
        token = None
        if hasattr(info.context.headers, 'environ'):
            if "HTTP_AUTHORIZATION" in info.context.headers.environ:
                token = parse_token(info.context.headers.environ["HTTP_AUTHORIZATION"])

        if not token:
            raise ValueError("Authorization header not provided. Must have a valid session to query for collaborators")

        default_remote = lb.labmanager_config.config['git']['default_remote']
        admin_service = None
        for remote in lb.labmanager_config.config['git']['remotes']:
            if default_remote == remote:
                admin_service = lb.labmanager_config.config['git']['remotes'][remote]['admin_service']
                break

        if not admin_service:
            raise ValueError('admin_service could not be found')

        # Configure git creds
        mgr = GitLabManager(default_remote, admin_service, access_token=token)
        mgr.configure_git_credentials(default_remote, username)

        if visibility not in ['public', 'private']:
            raise ValueError(f'Visibility must be either "public" or "private";'
                             f'("{visibility}" invalid)')
        mgr.set_visibility(namespace=owner, labbook_name=labbook_name, visibility=visibility)

        cursor = base64.b64encode(f"{0}".encode('utf-8'))
        lbedge = LabbookConnection.Edge(node=LabbookObject(owner=lb.owner['username'], name=labbook_name),
                                        cursor=cursor)
        return SetVisibility(new_labbook_edge=lbedge)
