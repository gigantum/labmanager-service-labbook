# Copyright (c) 2017 FlashX, LLC
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
import pytest

import os
from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_working_dir_populated_scoped, fixture_test_file
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from lmcommon.fixtures import ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_BASE, ENV_UNIT_TEST_REV
from lmcommon.files import FileOperations
from lmcommon.environment import ComponentManager
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityRecord, ActivityType


import graphene

from lmcommon.labbook import LabBook
from lmcommon.fixtures import remote_labbook_repo
from lmcommon.gitlib.git import GitAuthor


class TestLabBookOverviewQueries(object):
    def test_empty_package_counts(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's package manager dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook4", description="my first labbook10000")

        query = """
                    {
                      labbook(owner: "default", name: "labbook4") {
                        overview {
                          numAptPackages
                          numConda2Packages
                          numConda3Packages
                          numPipPackages
                          numCustomDependencies
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_package_counts(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's package manager dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook5", description="my first labbook10000")

        cm = ComponentManager(lb)
        # Add packages
        cm.add_packages("apt", [{"manager": "apt", "package": "docker", "version": ""}])
        pkgs = [{"manager": "pip", "package": "requests", "version": "1.3"},
                {"manager": "pip", "package": "numpy", "version": "1.12"}]
        cm.add_packages('pip', pkgs)

        pkgs = [{"manager": "conda2", "package": "requests", "version": "1.3"},
                {"manager": "conda2", "package": "numpy", "version": "1.12"},
                {"manager": "conda2", "package": "matplotlib", "version": "1.12"},
                {"manager": "conda2", "package": "plotly", "version": "1.12"}]
        cm.add_packages('conda2', pkgs)

        pkgs = [{"manager": "conda3", "package": "networkx", "version": "1.3"},
                {"manager": "conda3", "package": "nibabel", "version": "1.3"},
                {"manager": "conda3", "package": "scipy", "version": "1.12"}]
        cm.add_packages('conda3', pkgs)

        query = """
                    {
                      labbook(owner: "default", name: "labbook5") {
                        overview {
                          numAptPackages
                          numConda2Packages
                          numConda3Packages
                          numPipPackages
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_custom_counts(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's package manager dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook55", description="my first labbook10000")

        cm = ComponentManager(lb)
        # Add packages
        cm.add_component("custom", ENV_UNIT_TEST_REPO, "pillow", 0)
        cm.add_component("custom", ENV_UNIT_TEST_REPO, "noop-2", 0)
        cm.add_component("custom", ENV_UNIT_TEST_REPO, "noop-1", 0)

        query = """
                    {
                      labbook(owner: "default", name: "labbook55") {
                        overview {
                          numAptPackages
                          numConda2Packages
                          numConda3Packages
                          numPipPackages
                          numCustomDependencies
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_recent_activity(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test paging through activity records"""
        lb = LabBook(fixture_working_dir[0], author=GitAuthor(name="tester", email="tester@test.com"))
        lb.new(owner={"username": "default"}, name="labbook11", description="my test description")
        FileOperations.insert_file(lb, "code", fixture_test_file)

        # fake activity
        store = ActivityStore(lb)
        adr1 = ActivityDetailRecord(ActivityDetailType.CODE)
        adr1.show = False
        adr1.importance = 100
        adr1.add_value("text/plain", "first")

        ar = ActivityRecord(ActivityType.CODE,
                            show=False,
                            message="ran some code",
                            importance=50,
                            linked_commit="asdf")

        ar.add_detail_object(adr1)

        # Create Activity Record
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "input", '/tmp/test_file.txt')
        lb.makedir("input/test")
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "input", '/tmp/test_file.txt', "test")
        lb.makedir("input/test2")
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "input", '/tmp/test_file.txt', "test2")
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        store.create_activity_record(ar)
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "output", '/tmp/test_file.txt')

        # Get all records at once with no pagination args and verify cursors look OK directly
        query = """
                    {
                      labbook(owner: "default", name: "labbook11") {
                        overview {
                          recentActivity {
                            message
                            type
                            show
                            importance
                            tags
                          }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_no_remote_url(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's remote url without publish"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook6", description="my first labbook10000")

        query = """
                    {
                      labbook(owner: "default", name: "labbook6") {
                        overview {
                          remoteUrl
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))
