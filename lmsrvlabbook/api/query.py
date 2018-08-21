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
from typing import List
import graphene

from lmcommon.logging import LMLogger
from lmcommon.configuration import Configuration
from lmcommon.dispatcher import Dispatcher
from lmcommon.environment import ComponentRepository
from lmcommon.environment.utils import get_package_manager
from lmcommon.labbook.schemas import CURRENT_SCHEMA

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.objects.labbook import Labbook
from lmsrvlabbook.api.objects.labbooklist import LabbookList
from lmsrvlabbook.api.objects.basecomponent import BaseComponent
from lmsrvlabbook.api.objects.customcomponent import CustomComponent
from lmsrvlabbook.api.objects.packagecomponent import PackageComponent
from lmsrvlabbook.api.objects.jobstatus import JobStatus
from lmsrvlabbook.api.connections.environment import BaseComponentConnection, CustomComponentConnection
from lmsrvlabbook.api.connections.jobstatus import JobStatusConnection

from lmsrvcore.api.objects.user import UserIdentity


logger = LMLogger.get_logger()


class LabbookQuery(graphene.ObjectType):
    """Entry point for all LabBook queryable fields"""

    # TODO - Put all these fields in alphabetical order?

    # Create instance of the LabBook dataloader for use across all objects within this query instance

    # Node Fields for Relay
    node = graphene.relay.Node.Field()

    # Return app build date and hash
    build_info = graphene.String()

    # Return whether this has CUDA installed and can run GPU-enabled projects
    cuda_available = graphene.Boolean()

    labbook = graphene.Field(Labbook, owner=graphene.String(), name=graphene.String())

    # This indicates the most-recent labbook schema version.
    # Nominal usage of this field is to see if any given labbook is behind this version.
    # Any new labbook will be created with this schema version.
    current_labbook_schema_version = graphene.Int()

    # Used to query for specific background jobs.
    # job_id is in the format of `rq:job:uuid`, though it should never need to be parsed.
    job_status = graphene.Field(JobStatus, job_id=graphene.String())

    # All background jobs in the system: Queued, Completed, Failed, and Started.
    background_jobs = graphene.relay.ConnectionField(JobStatusConnection)

    # A field to interact with listing labbooks locally and remote
    labbook_list = graphene.Field(LabbookList)

    # Base Image Repository Interface
    available_bases = graphene.relay.ConnectionField(BaseComponentConnection)

    # Currently not fully supported, but will be added in the future.
    # available_base_image_versions = graphene.relay.ConnectionField(BaseImageConnection, repository=graphene.String(),
    #                                                                namespace=graphene.String(),
    #                                                                component=graphene.String())

    # Custom Dependency Repository Interface
    available_custom_dependencies = graphene.relay.ConnectionField(CustomComponentConnection)

    # Package Query for validating packages and getting latest versions
    package = graphene.Field(PackageComponent,
                             manager=graphene.String(),
                             package=graphene.String(),
                             version=graphene.String(default_value=""))

    # Get the current logged in user identity, primarily used when running offline
    user_identity = graphene.Field(UserIdentity)

    def resolve_build_info(self, info):
        """Return this LabManager build info (hash, build timestamp, etc)"""
        # TODO - CUDA version should possibly go in here
        build_info = Configuration().config.get('build_info') or {}
        return '-'.join([build_info.get('application', 'UnknownDate'),
                         build_info.get('revision', 'UnknownHash'),
                         build_info.get('built_on', 'UnknownApplication')])

    def resolve_cuda_available(self, info):
        """Return the CUDA version of the host machine. Non-null implies GPU available"""
        if Configuration().host_cuda_version:
            return False
        else:
            return True

    def resolve_labbook(self, info, owner: str, name: str):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            owner(str): Username of the owner (aka namespace)
            name(str): Name of the LabBook
            _dataloader: A dataloader instance

        Returns:
            Labbook
        """
        # Load the labbook data via a dataloader
        return Labbook(id="{}&{}".format(owner, name),
                       name=name, owner=owner)

    def resolve_current_labbook_schema_version(self, info):
        """Return the current LabBook schema version"""
        return CURRENT_SCHEMA

    def resolve_labbook_list(self, info):
        """Return a labbook list object, which is just a container so the id is empty"""
        return LabbookList(id="")

    def resolve_job_status(self, info, job_id: str):
        """Method to return a graphene Labbok instance based on the name

        Uses the "currently logged in" user

        Args:
            job_id(dict): Contains user details

        Returns:
            JobStatus
        """
        return JobStatus(job_id)

    def resolve_background_jobs(self, info, **kwargs):
        """Method to return a all background jobs the system is aware of: Queued, Started, Finished, Failed.

        Returns:
            list(JobStatus)
        """
        job_dispatcher = Dispatcher()

        edges: List[str] = [j.job_key.key_str for j in job_dispatcher.all_jobs]
        cursors = [base64.b64encode(f"{str(cnt)}".encode('utf-8')) for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            edge_objs.append(JobStatusConnection.Edge(node=JobStatus(edge), cursor=cursor))

        return JobStatusConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_bases(self, info, **kwargs):
        """Method to return a all graphene BaseImages that are available

        Returns:
            list(Labbook)
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("base")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            edge_objs.append(BaseComponentConnection.Edge(node=BaseComponent(repository=edge['###repository###'],
                                                                             component_id=edge['id'],
                                                                             revision=int(edge['revision'])),
                                                          cursor=cursor))

        return BaseComponentConnection(edges=edge_objs, page_info=lbc.page_info)

    # Currently not fully supported, but will be added in the future.
    # def resolve_available_base_image_versions(self, info, repository, namespace, component, **kwargs):
    #     """Method to return a all graphene BaseImages that are available
    #
    #     Returns:
    #         list(Labbook)
    #     """
    #     repo = ComponentRepository()
    #     edges = repo.get_component_versions("base_image",
    #                                         repository,
    #                                         namespace,
    #                                         component)
    #     cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]
    #
    #     # Process slicing and cursor args
    #     lbc = ListBasedConnection(edges, cursors, kwargs)
    #     lbc.apply()
    #
    #     # Get BaseImage instances
    #     edge_objs = []
    #     for edge, cursor in zip(lbc.edges, lbc.cursors):
    #         id_data = {'component_data': edge[1],
    #                    'component_class': 'base_image',
    #                    'repo': repository,
    #                    'namespace': namespace,
    #                    'component': component,
    #                    'version': edge[0]
    #                    }
    #         edge_objs.append(BaseImageConnection.Edge(node=BaseImage.create(id_data), cursor=cursor))
    #
    #     return BaseImageConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_available_custom_dependencies(self, info, **kwargs):
        """Method to return all graphene CustomDependencies that are available (at the latest version)

        Returns:
            CustomDependencyConnection
        """
        repo = ComponentRepository()
        edges = repo.get_component_list("custom")
        cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in enumerate(edges)]

        # Process slicing and cursor args
        lbc = ListBasedConnection(edges, cursors, kwargs)
        lbc.apply()

        # Get BaseImage instances
        edge_objs = []
        for edge, cursor in zip(lbc.edges, lbc.cursors):
            edge_objs.append(CustomComponentConnection.Edge(node=CustomComponent(repository=edge['###repository###'],
                                                                                 component_id=edge['id'],
                                                                                 revision=edge['revision']),
                                                            cursor=cursor))

        return CustomComponentConnection(edges=edge_objs, page_info=lbc.page_info)

    def resolve_user_identity(self, info):
        """Method to return a graphene UserIdentity instance based on the current logged (both on & offline) user

        Returns:
            UserIdentity
        """
        return UserIdentity()
