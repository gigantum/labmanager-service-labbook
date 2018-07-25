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
import graphene
import os
import glob

from lmcommon.logging import LMLogger
from lmcommon.activity import ActivityStore

from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api.interfaces import GitRepository

from lmsrvlabbook.api.objects.activity import ActivityRecordObject

logger = LMLogger.get_logger()


class LabbookOverview(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """A type representing the overview of a LabBook

    It contains counts for all package managers, the last 3 activity records with show=True
    """
    # Class attribute to store package manager counts
    _package_manager_counts = None

    # Package counts
    num_apt_packages = graphene.Int()
    num_conda2_packages = graphene.Int()
    num_conda3_packages = graphene.Int()
    num_pip_packages = graphene.Int()
    num_custom_dependencies = graphene.Int()

    # List last 4 activity items that have show=True
    recent_activity = graphene.List(ActivityRecordObject)

    # Share URL if the LabBook has been published
    remote_url = graphene.String()

    def _get_all_package_manager_counts(self, labbook):
        """helper method to get all package manager counts in a LabBook

        Returns:
            None
        """
        pkg_dir = os.path.join(labbook.root_dir, ".gigantum", "env", "package_manager")

        self._package_manager_counts = {'apt': 0,
                                        'conda2': 0,
                                        'conda3': 0,
                                        'pip': 0}

        for f in glob.glob(os.path.join(pkg_dir, "*.yaml")):
            f = os.path.basename(f)
            mgr, _ = f.split('_', 1)

            self._package_manager_counts[mgr] = self._package_manager_counts[mgr] + 1

        return self._package_manager_counts

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name = id.split("&")

        return LabbookOverview(owner=owner, name=name)

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name:
                raise ValueError("Resolving a LabbookOverview Node ID requires owner and name to be set")

            self.id = f"{self.owner}&{self.name}"

        return self.id

    def resolve_num_apt_packages(self, info):
        """Resolver for getting number of apt packages in the labbook"""
        if self._package_manager_counts is None:
            return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
                lambda labbook: self._get_all_package_manager_counts(labbook)['apt'])

        return self._package_manager_counts['apt']

    def resolve_num_conda2_packages(self, info):
        """Resolver for getting number of conda2 packages in the labbook"""
        if self._package_manager_counts is None:
            return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
                lambda labbook: self._get_all_package_manager_counts(labbook)['conda2'])

        return self._package_manager_counts['conda2']

    def resolve_num_conda3_packages(self, info):
        """Resolver for getting number of conda3 packages in the labbook"""
        if self._package_manager_counts is None:
            return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
                lambda labbook: self._get_all_package_manager_counts(labbook)['conda3'])

        return self._package_manager_counts['conda3']

    def resolve_num_pip_packages(self, info):
        """Resolver for getting number of pip packages in the labbook"""
        if self._package_manager_counts is None:
            return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
                lambda labbook: self._get_all_package_manager_counts(labbook)['pip'])

        return self._package_manager_counts['pip']

    @staticmethod
    def helper_resolve_num_custom_dependencies(labbook):
        """Helper to count the number of custom deps"""
        custom_dir = os.path.join(labbook.root_dir, ".gigantum", "env", "custom")
        count = len([x for x in glob.glob(os.path.join(custom_dir, "*.yaml"))])
        return count

    def resolve_num_custom_dependencies(self, info):
        """Resolver for getting number of custom dependencies in the labbook"""
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_num_custom_dependencies(labbook))

    def help_resolve_recent_activity(self, labbook):
        """Method to create 4 activity records with show=True"""
        # Create instance of ActivityStore for this LabBook
        store = ActivityStore(labbook)

        records = list()
        # Get 4 records with show=True
        after = None
        while len(records) < 4:
            items = store.get_activity_records(first=4, after=after)

            if not items:
                # if no more items, continue
                break

            for item in items:
                if item.show is True and len(item.detail_objects) > 0:
                    ar = ActivityRecordObject(id=f"{self.owner}&{self.name}&{item.commit}",
                                              owner=self.owner,
                                              name=self.name,
                                              commit=item.commit,
                                              _activity_record=item)
                    records.append(ar)
                    if len(records) >= 4:
                        break

                # Set after cursor to last commit
                after = item.commit

        return records

    def resolve_recent_activity(self, info):
        """Resolver for getting recent important activity"""
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.help_resolve_recent_activity(labbook))
    
    @staticmethod
    def helper_resolve_remote_url(labbook):
        if len(labbook.git.repo.remotes) > 0:
            remote = labbook.git.repo.remotes.origin.url
            return remote.replace(".git", "")
        else:
            return None

    def resolve_remote_url(self, info):
        """Resolver for getting the remote_url in the labbook"""
        return info.context.labbook_loader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").then(
            lambda labbook: self.helper_resolve_remote_url(labbook))
