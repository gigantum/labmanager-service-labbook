
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
import graphene
import requests
import base64

from docker.errors import ImageNotFound, NotFound

from lmcommon.dispatcher import Dispatcher
from lmcommon.environment.componentmanager import ComponentManager
from lmcommon.configuration import get_docker_client
from lmcommon.logging import LMLogger
from lmcommon.container.utils import infer_docker_image_name

from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.connections import ListBasedConnection

from lmsrvlabbook.api.connections.environment import CustomComponentConnection, PackageComponentConnection
from lmsrvlabbook.api.objects.envcomponents import BaseComponent, PackageComponent, CustomComponent
from lmsrvlabbook.dataloader.package import PackageLatestVersionLoader

logger = LMLogger.get_logger()


class ImageStatus(graphene.Enum):
    """An enumeration for Docker image status"""

    # The image has not be built locally yet
    DOES_NOT_EXIST = 0

    # The image is being built
    BUILD_IN_PROGRESS = 1

    # The task to build the image is stuck in queued
    BUILD_QUEUED = 99

    # The image has been built and the Dockerfile has yet to change
    EXISTS = 2

    # The image has been built and the Dockerfile has been edited
    STALE = 3

    # The image failed to build
    BUILD_FAILED = 4


class ContainerStatus(graphene.Enum):
    """An enumeration for container image status"""

    # The container is not running
    NOT_RUNNING = 0

    # The container is starting
    STARTING = 1

    # The container is running
    RUNNING = 2


class Environment(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type that represents the Environment for a LabBook"""
    # The name of the current branch
    image_status = graphene.Field(ImageStatus)

    # The name of the current branch
    container_status = graphene.Field(ContainerStatus)

    # The LabBook's Base Component
    base = graphene.Field(BaseComponent)

    # The LabBook's Package manager installed dependencies
    package_dependencies = graphene.ConnectionField(PackageComponentConnection)

    # The LabBook's Custom dependencies
    custom_dependencies = graphene.ConnectionField(CustomComponentConnection,
                                                   deprecation_reason="Custom Dependencies have been replaced "
                                                                      "with custom docker interface")

    # A custom docker snippet to be run after all other dependencies and bases have been added.
    docker_snippet = graphene.String()

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name = id.split("&")

        return Environment(id=f"{owner}&{name}", name=name, owner=owner)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.owner or not self.name:
            raise ValueError("Resolving a Environment Node ID requires owner and name to be set")

        return f"{self.owner}&{self.name}"

    def helper_resolve_image_status(self, labbook):
        """Helper to resolve the image status of a labbook"""
        labbook_image_key = infer_docker_image_name(labbook_name=self.name, owner=self.owner,
                                                    username=get_logged_in_username())

        dispatcher = Dispatcher()
        lb_jobs = [dispatcher.query_task(j.job_key) for j in dispatcher.get_jobs_for_labbook(labbook.key)]

        for j in lb_jobs:
            logger.debug("Current job for labbook: status {}, meta {}".format(j.status, j.meta))

        # First, check if image exists or not -- The first step of building an image untags any existing ones.
        # Therefore, we know that if one exists, there most likely is not one being built.
        try:
            client = get_docker_client()
            client.images.get(labbook_image_key)
            image_status = ImageStatus.EXISTS
        except (ImageNotFound, requests.exceptions.ConnectionError):
            image_status = ImageStatus.DOES_NOT_EXIST

        if any([j.status == 'failed' and j.meta.get('method') == 'build_image' for j in lb_jobs]):
            logger.debug("Image status for {} is BUILD_FAILED".format(labbook.key))
            if image_status == ImageStatus.EXISTS:
                # The indication that there's a failed job is probably lingering from a while back, so don't
                # change the status to FAILED. Only do that if there is no Docker image.
                logger.debug(f'Got failed build_image for labbook {labbook.key}, but image exists.')
            else:
                image_status = ImageStatus.BUILD_FAILED

        if any([j.status in ['started'] and j.meta.get('method') == 'build_image' for j in lb_jobs]):
            logger.debug(f"Image status for {labbook.key} is BUILD_IN_PROGRESS")
            # build_image being in progress takes precedence over if image already exists (unlikely event).
            if image_status == ImageStatus.EXISTS:
                logger.warning(f'Got build_image for labbook {labbook.key}, but image exists.')
            image_status = ImageStatus.BUILD_IN_PROGRESS

        if any([j.status in ['queued'] and j.meta.get('method') == 'build_image' for j in lb_jobs]):
            logger.warning(f"build_image for {labbook.key} stuck in queued state")
            image_status = ImageStatus.BUILD_QUEUED

        return image_status.value

    def resolve_image_status(self, info):
        """Resolve the image_status field"""
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_image_status(labbook))

    def resolve_container_status(self, info):
        """Resolve the image_status field"""
        # Check if the container is running by looking up the container
        labbook_key = infer_docker_image_name(labbook_name=self.name, owner=self.owner,
                                              username=get_logged_in_username())

        try:
            client = get_docker_client()
            container = client.containers.get(labbook_key)
            if container.status == "running":
                container_status = ContainerStatus.RUNNING
            else:
                container_status = ContainerStatus.NOT_RUNNING
        except (NotFound, requests.exceptions.ConnectionError):
            container_status = ContainerStatus.NOT_RUNNING

        return container_status.value

    @staticmethod
    def helper_resolve_base(labbook):
        """Helper to resolve the base component object"""
        # Get base image data from the LabBook
        cm = ComponentManager(labbook)
        component_data = cm.base_fields

        if component_data:
            return BaseComponent(id=f"{component_data['###repository###']}&{component_data['id']}&{component_data['revision']}",
                                 repository=component_data['###repository###'],
                                 component_id=component_data['id'],
                                 revision=int(component_data['revision']),
                                 _component_data=component_data)
        else:
            return None

    def resolve_base(self, info):
        """Method to get the LabBook's base component

        Args:
            info:

        Returns:

        """
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_base(labbook))

    @staticmethod
    def helper_resolve_package_dependencies(labbook, kwargs):
        """Helper to resolve the packages"""
        cm = ComponentManager(labbook)
        edges = cm.get_component_list("package_manager")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, kwargs)
            lbc.apply()

            # Create version dataloader
            keys = [f"{k['manager']}&{k['package']}" for k in lbc.edges]
            vd = PackageLatestVersionLoader(keys, labbook, get_logged_in_username())

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                edge_objs.append(PackageComponentConnection.Edge(node=PackageComponent(_version_dataloader=vd,
                                                                                       manager=edge['manager'],
                                                                                       package=edge['package'],
                                                                                       version=edge['version'],
                                                                                       from_base=edge['from_base'],
                                                                                       is_valid=True,
                                                                                       schema=edge['schema']),
                                                                 cursor=cursor))

            return PackageComponentConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return PackageComponentConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                          has_previous_page=False))

    def resolve_package_dependencies(self, info, **kwargs):
        """Method to get the LabBook's package manager dependencies

        Args:
            info:

        Returns:

        """
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_package_dependencies(labbook, kwargs))

    @staticmethod
    def helper_resolve_custom_dependencies(labbook, kwargs):
        """Helper to generate custom dependencies (DEPRECATED)"""
        cm = ComponentManager(labbook)
        edges = cm.get_component_list("custom")

        if edges:
            cursors = [base64.b64encode("{}".format(cnt).encode("UTF-8")).decode("UTF-8") for cnt, x in
                       enumerate(edges)]

            # Process slicing and cursor args
            lbc = ListBasedConnection(edges, cursors, kwargs)
            lbc.apply()

            # Get DevEnv instances
            edge_objs = []
            for edge, cursor in zip(lbc.edges, lbc.cursors):
                edge_objs.append(CustomComponentConnection.Edge(node=CustomComponent(repository=edge['###repository###'],
                                                                                     component_id=edge['id'],
                                                                                     revision=edge['revision']),
                                                                cursor=cursor))

            return CustomComponentConnection(edges=edge_objs, page_info=lbc.page_info)

        else:
            return CustomComponentConnection(edges=[], page_info=graphene.relay.PageInfo(has_next_page=False,
                                                                                         has_previous_page=False))

    def resolve_custom_dependencies(self, info, **kwargs):
        """Method to get the LabBook's custom dependencies

        Args:
            info:

        Returns:

        """
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_custom_dependencies(labbook, kwargs))

    @staticmethod
    def helper_resolve_docker_snippet(labbook):
        """Helper to get custom docker snippet"""
        cm = ComponentManager(labbook)
        docker_components = cm.get_component_list('docker')
        if len(docker_components) == 1:
            return '\n'.join(docker_components[0]['content'])
        elif len(docker_components) > 1:
            raise ValueError('There should only be one custdom docker component')
        else:
            return ""

    def resolve_docker_snippet(self, info):
        """Method to resolve  the docker snippet for this labbook. Right now only 1 snippet is supported"""
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_docker_snippet(labbook))
