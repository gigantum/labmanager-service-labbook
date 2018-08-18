
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

from lmcommon.environment import ComponentRepository
from lmcommon.logging import LMLogger

logger = LMLogger.get_logger()


class BaseComponent(graphene.ObjectType, interfaces=(graphene.relay.Node,)):
    """A type that represents a Base Image Environment Component"""
    # The loaded yaml data
    _component_data = None

    # The Component schema version
    schema = graphene.Int()

    # The name of the component repository where this Base is stored
    repository = graphene.String(required=True)

    # id field from the Base component definition file
    component_id = graphene.String(required=True)

    # Revision of the component
    revision = graphene.Int(required=True)

    # Human readable name
    name = graphene.String()

    # Short description of the Base
    description = graphene.String()

    # Arbitrary markdown description of the base
    readme = graphene.String()

    # Tags that can be used when searching/filtering components
    tags = graphene.List(graphene.String)

    # Base64 encoded image
    icon = graphene.String()

    # The class of Operating System used (e.g. ubuntu)
    os_class = graphene.String()

    # The release of the Operating System used (e.g. 16.04)
    os_release = graphene.String()

    # License applied to the base
    license = graphene.String()

    # Url to more documentation or info about the base
    url = graphene.String()

    # List of installed programming languages that are available to the user
    languages = graphene.List(graphene.String)

    # List of installed development tools that are available to the user
    development_tools = graphene.List(graphene.String)

    # List of installed package managers that are available to the user
    package_managers = graphene.List(graphene.String)

    # List of pre-installed packages in the format <package manager>|<package name>|<package version>
    installed_packages = graphene.List(graphene.String)

    # The container registry server used to pull the image
    docker_image_server = graphene.String()

    # The namespace to used on the container registry server when pulling the image
    docker_image_namespace = graphene.String()

    # The repo to use on the container registry server when pulling the image
    docker_image_repository = graphene.String()

    # The image tag to use on the container registry server when pulling the image
    docker_image_tag = graphene.String()

    def _format_package(self, package_str):
        """Helper method to format package strings

        Args:
            package_str(str): the package string with the version include

        Returns:
            string
        """
        if "=" in package_str:
            package_str = package_str.replace('==', '|').replace('=', '|')
        else:
            package_str = f"{package_str}|latest"

        return package_str

    def _load_component_info(self):
        """Private method to retrieve file info for a given key"""
        if not self._component_data:
            repo = ComponentRepository()

            self._component_data = repo.get_component("base", self.repository, self.component_id, self.revision)

        self.schema = self._component_data['schema']
        self.name = self._component_data['name']
        self.description = self._component_data['description']
        self.readme = self._component_data['readme']
        self.tags = self._component_data['tags']
        self.icon = self._component_data['icon']
        self.os_class = self._component_data['os_class']
        self.os_release = self._component_data['os_release']
        self.license = self._component_data['license']
        self.url = self._component_data['url']
        self.languages = self._component_data['languages']
        self.development_tools = self._component_data['development_tools']
        self.docker_image_server = self._component_data['image']['server']
        self.docker_image_namespace = self._component_data['image']['namespace']
        self.docker_image_repository = self._component_data['image']['repository']
        self.docker_image_tag = self._component_data['image']['tag']

        self.package_managers = list()
        self.installed_packages = list()
        for entry in self._component_data['package_managers']:
            for package_manager in entry:
                self.package_managers.append(package_manager)
                if entry[package_manager]:
                    for package in entry[package_manager]:
                        self.installed_packages.append(f"{package_manager}|{self._format_package(package)}")

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        repository, component_id, revision = id.split("&")

        return BaseComponent(id=f"{repository}&{component_id}&{revision}",
                             repository=repository, component_id=component_id, revision=int(revision))

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.repository or not self.component_id or self.revision is None:
            raise ValueError("Resolving a BaseComponent ID requires repository, component_id and revision to be set")

        return f"{self.repository}&{self.component_id}&{self.revision}"

    def resolve_name(self, info):
        """Resolve the name field"""
        if self.name is None:
            self._load_component_info()
        return self.name

    def resolve_schema(self, info):
        """Resolve the schema field"""
        if self.schema is None:
            self._load_component_info()
        return self.schema

    def resolve_description(self, info):
        """Resolve the description field"""
        if self.description is None:
            self._load_component_info()
        return self.description

    def resolve_readme(self, info):
        """Resolve the readme field"""
        if self.readme is None:
            self._load_component_info()
        return self.readme

    def resolve_tags(self, info):
        """Resolve the tags field"""
        if self.tags is None:
            self._load_component_info()
        return self.tags

    def resolve_icon(self, info):
        """Resolve the icon field"""
        if self.icon is None:
            self._load_component_info()
        return self.icon

    def resolve_os_class(self, info):
        """Resolve the os_class field"""
        if self.os_class is None:
            self._load_component_info()
        return self.os_class

    def resolve_os_release(self, info):
        """Resolve the os_release field"""
        if self.os_release is None:
            self._load_component_info()
        return self.os_release

    def resolve_license(self, info):
        """Resolve the license field"""
        if self.license is None:
            self._load_component_info()
        return self.license

    def resolve_url(self, info):
        """Resolve the url field"""
        if self.url is None:
            self._load_component_info()
        return self.url

    def resolve_languages(self, info):
        """Resolve the languages field"""
        if self.languages is None:
            self._load_component_info()
        return self.languages

    def resolve_development_tools(self, info):
        """Resolve the development_tools field"""
        if self.development_tools is None:
            self._load_component_info()
        return self.development_tools

    def resolve_docker_image_server(self, info):
        """Resolve the docker_image_server field"""
        if self.docker_image_server is None:
            self._load_component_info()
        return self.docker_image_server

    def resolve_docker_image_namespace(self, info):
        """Resolve the docker_image_namespace field"""
        if self.docker_image_namespace is None:
            self._load_component_info()
        return self.docker_image_namespace

    def resolve_docker_image_repository(self, info):
        """Resolve the docker_image_repository field"""
        if self.docker_image_repository is None:
            self._load_component_info()
        return self.docker_image_repository

    def resolve_docker_image_tag(self, info):
        """Resolve the docker_image_tag field"""
        if self.docker_image_tag is None:
            self._load_component_info()
        return self.docker_image_tag

    def resolve_package_managers(self, info):
        """Resolve the package_managers field"""
        if self.package_managers is None:
            self._load_component_info()
        return self.package_managers

    def resolve_installed_packages(self, info):
        """Resolve the installed_packages field"""
        if self.installed_packages is None:
            self._load_component_info()
        return self.installed_packages


class PackageComponentInput(graphene.InputObjectType):
    """An input type to support Batch interfaces that use Package Components"""

    # The name of the package manager
    manager = graphene.String(required=True)

    # The name of the package
    package = graphene.String(required=True)

    # The desired version of the package
    version = graphene.String()


class PackageComponent(graphene.ObjectType, interfaces=(graphene.relay.Node,)):
    """A type that represents a Package Manager based Environment Component"""
    # The loaded yaml data
    _component_data = None

    # The version dataloader used to coalesce conda commands
    _version_dataloader = None

    # The Component schema version
    schema = graphene.Int()

    # The name of the package manager
    manager = graphene.String(required=True)

    # The name of the package
    package = graphene.String(required=True)

    # The current version of the package
    version = graphene.String(required=True)

    # The latest available version of the package
    latest_version = graphene.String()

    # Flag indicating if the component is in the Base
    from_base = graphene.Boolean()

    # Flag indicating if the package name and version has been validated
    is_valid = graphene.Boolean(default_value=False)

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        manager, package, version = id.split("&")

        return PackageComponent(id=f"{manager}&{package}&{version}",
                                manager=manager, package=package, version=version)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.manager or not self.package or self.version is None:
            raise ValueError("Resolving a PackageComponent ID requires manager, package and version to be set")

        return f"{self.manager}&{self.package}&{self.version}"

    def resolve_latest_version(self, info):
        """Resolve the latest_version field"""
        if self.latest_version is not None:
            return self.latest_version

        if not self._version_dataloader:
            # No dataloader is available, so load manually
            logger.warning("Cannot query for latest version of {self.package} - no labbook context")
            return None

        # If you get here, load via version dataloader (which has labbook context)
        return self._version_dataloader.load(f"{self.manager}&{self.package}")

    def resolve_from_base(self, info):
        """Resolve the from_base field"""
        if self.from_base is None:
            # Assume not from base if value is not set on construction
            return False
        else:
            return self.from_base


class CustomComponent(graphene.ObjectType, interfaces=(graphene.relay.Node,)):
    """A type that represents a Custom Dependency Environment Component"""
    # The loaded yaml data
    _component_data = None

    # The Component schema version
    schema = graphene.Int()

    # The name of the component repository where this Base is stored
    repository = graphene.String(required=True)

    # id field from the Base component definition file
    component_id = graphene.String(required=True)

    # Revision of the component
    revision = graphene.Int(required=True)

    # Human readable name
    name = graphene.String()

    # Short description of the Base
    description = graphene.String()

    # Tags that can be used when searching/filtering components
    tags = graphene.List(graphene.String)

    # License applied to the underlying component being installed
    license = graphene.String()

    # Required OS base class to add the component
    os_base_class = graphene.String()

    # Url to more documentation or info about the base
    url = graphene.String()

    # List of installed package managers that are available to the user
    required_package_managers = graphene.List(graphene.String)

    # Custom snippet to insert into the LabBook's Dockerfile
    docker_snippet = graphene.String()

    def _load_component_info(self):
        """Private method to retrieve file info for a given key"""
        if not self._component_data:
            repo = ComponentRepository()

            self._component_data = repo.get_component("custom", self.repository, self.component_id, self.revision)

        self.schema = self._component_data['schema']
        self.name = self._component_data['name']
        self.description = self._component_data['description']
        self.tags = self._component_data.get('tags')
        self.license = self._component_data.get('license')
        self.url = self._component_data.get('url')
        self.os_base_class = self._component_data.get('os_base_class')
        self.required_package_managers = self._component_data.get('required_package_managers')
        self.docker_snippet = self._component_data['docker']

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        repository, component_id, revision = id.split("&")

        return CustomComponent(id=f"{repository}&{component_id}&{revision}",
                               repository=repository, component_id=component_id, revision=int(revision))

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.repository or not self.component_id or self.revision is None:
            raise ValueError("Resolving a CustomComponent ID requires repository, component_id and revision to be set")

        return f"{self.repository}&{self.component_id}&{self.revision}"

    def resolve_schema(self, info):
        """Resolve the schema field"""
        if self.schema is None:
            self._load_component_info()
        return self.schema

    def resolve_name(self, info):
        """Resolve the name field"""
        if self.name is None:
            self._load_component_info()
        return self.name

    def resolve_description(self, info):
        """Resolve the description field"""
        if self.description is None:
            self._load_component_info()
        return self.description

    def resolve_version(self, info):
        """Resolve the version field"""
        if self.version is None:
            self._load_component_info()
        return self.version

    def resolve_tags(self, info):
        """Resolve the tags field"""
        if self.tags is None:
            self._load_component_info()
        return self.tags

    def resolve_license(self, info):
        """Resolve the license field"""
        if self.license is None:
            self._load_component_info()
        return self.license

    def resolve_url(self, info):
        """Resolve the url field"""
        if self.url is None:
            self._load_component_info()
        return self.url

    def resolve_os_base_class(self, info):
        """Resolve the os_base_class field"""
        if self.os_base_class is None:
            self._load_component_info()
        return self.os_base_class

    def resolve_required_package_managers(self, info):
        """Resolve the required_package_managers field"""
        if self.required_package_managers is None:
            self._load_component_info()
        return self.required_package_managers

    def resolve_docker_snippet(self, info):
        """Resolve the docker_snippet field"""
        if self.docker_snippet is None:
            self._load_component_info()
        return self.docker_snippet
