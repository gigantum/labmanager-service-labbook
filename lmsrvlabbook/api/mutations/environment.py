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
import glob
import os
import base64

from lmcommon.logging import LMLogger
from lmcommon.labbook import LabBook
from lmcommon.environment import ComponentManager
from lmcommon.labbook.schemas import CURRENT_SCHEMA
from lmsrvcore.auth.user import get_logged_in_username, get_logged_in_author
from lmsrvlabbook.api.objects.packagecomponent import PackageComponent, PackageComponentInput
from lmsrvlabbook.api.objects.customcomponent import CustomComponent
from lmsrvlabbook.api.objects.environment import Environment
from lmsrvlabbook.api.connections.environment import CustomComponentConnection, PackageComponentConnection

logger = LMLogger.get_logger()


class AddPackageComponents(graphene.relay.ClientIDMutation):
    """Mutation to add or update packages to labbook

    You MUST have previously validated the package information or errors can occur at build time.
    You MUST include a version, since auto-addition of a package version is done during validation.
    """

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        packages = graphene.List(PackageComponentInput)

    new_package_component_edges = graphene.List(PackageComponentConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, packages, client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        manager = list(set([x['manager'] for x in packages]))
        if len(manager) != 1:
            raise ValueError("Only batch add packages via 1 package manager at a time.")
        manager = manager[0]

        # Set the cursor to the end of the collection of packages
        glob_path = os.path.join(lb.root_dir, '.gigantum', 'env', 'package_manager', f"{manager}*")
        cursor = len(glob.glob(glob_path))

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.add_packages(package_manager=manager, packages=packages, from_base=False, force=True)

        new_edges = list()
        for cnt, pkg in enumerate(packages):
            new_edges.append(PackageComponentConnection.Edge(node=PackageComponent(manager=manager,
                                                                                   package=pkg["package"],
                                                                                   version=pkg["version"],
                                                                                   schema=CURRENT_SCHEMA),
                             cursor=base64.b64encode(str(cursor+cnt).encode()).decode()))

        return AddPackageComponents(new_package_component_edges=new_edges)


class RemovePackageComponents(graphene.relay.ClientIDMutation):
    """Mutation to remove packages from labbook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        manager = graphene.String(required=True)
        packages = graphene.List(graphene.String, required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, manager, packages,
                               client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.remove_packages(package_manager=manager, package_names=packages)

        return RemovePackageComponents(success=True)


class AddCustomDocker(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        docker_content = graphene.String(required=True)

    updated_environment = graphene.Field(Environment)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, docker_content, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        docker_lines = [n for n in docker_content.strip().split('\n') if n]
        cm = ComponentManager(lb)
        cm.add_docker_snippet(cm.DEFAULT_CUSTOM_DOCKER_NAME, docker_lines)
        return AddCustomDocker(updated_environment=Environment(owner=owner, name=labbook_name))


class RemoveCustomDocker(graphene.relay.ClientIDMutation):
    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)

    updated_environment = graphene.Field(Environment)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, client_mutation_id=None):
        username = get_logged_in_username()
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        # TODO - Should we cehck if a custom docker component already exists?
        cm = ComponentManager(lb)
        cm.remove_docker_snippet(cm.DEFAULT_CUSTOM_DOCKER_NAME)
        return RemoveCustomDocker(updated_environment=Environment(owner=owner, name=labbook_name))


class AddCustomComponent(graphene.relay.ClientIDMutation):
    """Mutation to add a new environment component to a LabBook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        repository = graphene.String(required=True)
        component_id = graphene.String(required=True)
        revision = graphene.Int(required=True)

    new_custom_component_edge = graphene.Field(lambda: CustomComponentConnection.Edge)

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, repository, component_id, revision,
                               client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.add_component("custom", repository, component_id, revision, force=True)

        # TODO: get cursor by checking how many packages are already installed

        new_edge = CustomComponentConnection.Edge(node=CustomComponent(repository=repository, component_id=component_id,
                                                                       revision=revision),
                                                  cursor=0)

        return AddCustomComponent(new_custom_component_edge=new_edge)


class RemoveCustomComponent(graphene.relay.ClientIDMutation):
    """Mutation to remove an environment component to a LabBook"""

    class Input:
        owner = graphene.String(required=True)
        labbook_name = graphene.String(required=True)
        repository = graphene.String(required=True)
        component_id = graphene.String(required=True)

    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, owner, labbook_name, repository, component_id, client_mutation_id=None):
        username = get_logged_in_username()

        # Load LabBook instance
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)

        # Create Component Manager
        cm = ComponentManager(lb)
        cm.remove_component("custom", repository, component_id)

        return RemoveCustomComponent(success=True)
