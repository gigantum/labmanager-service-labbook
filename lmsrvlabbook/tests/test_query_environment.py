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
import graphene
import pprint

from lmcommon.labbook import LabBook
from lmcommon.fixtures import ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_BASE, ENV_UNIT_TEST_REV
from lmcommon.environment import ComponentManager

from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir


class TestEnvironmentServiceQueries(object):
    def test_get_environment_status(self, fixture_working_dir, snapshot):
        """Test getting the a LabBook's environment status"""
        # Create labbooks
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook10", description="my first labbook10000")

        query = """
        {
          labbook(owner: "default", name: "labbook10") {
              environment {
                containerStatus
                imageStatus
              }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_base(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's base"""
        # Create labbook
        query = """
        mutation myCreateLabbook($name: String!, $desc: String!, $repository: String!, 
                                 $component_id: String!, $revision: Int!) {
          createLabbook(input: {name: $name, description: $desc, 
                                repository: $repository, 
                                componentId: $component_id, revision: $revision}) {
            labbook {
              id
              name
              description
            }
          }
        }
        """
        variables = {"name": "labbook-base-test", "desc": "my test 1",
                     "component_id": ENV_UNIT_TEST_BASE, "repository": ENV_UNIT_TEST_REPO,
                     "revision": ENV_UNIT_TEST_REV}
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query, variable_values=variables))

        query = """
                {
                  labbook(owner: "default", name: "labbook-base-test") {
                    name
                    description
                    environment {
                      base{                        
                        id
                        componentId
                        name
                        description
                        readme
                        tags
                        icon
                        osClass
                        osRelease
                        license
                        url
                        languages
                        developmentTools
                        dockerImageServer
                        dockerImageNamespace
                        dockerImageRepository
                        dockerImageTag
                        packageManagers
                      }
                    }
                  }
                }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_custom(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's custom dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook3", description="my first labbook10000")

        query = """
                    {
                      labbook(owner: "default", name: "labbook3") {
                        environment {
                         customDependencies { 
                            edges {
                              node {
                                id
                                schema
                                componentId
                                repository
                                revision
                                name
                                description                        
                                tags
                                license
                                url
                                requiredPackageManagers
                                dockerSnippet
                              }
                              cursor
                            }
                            pageInfo {
                              hasNextPage
                              hasPreviousPage
                            }
                         }
                       }  
                      }
                    }            
                    """
        # should be null
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        # Add a base image
        cm = ComponentManager(lb)
        cm.add_component("custom",
                         ENV_UNIT_TEST_REPO,
                         "pillow",
                         0)

        # Test again
        r2 = fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in r2
        snapshot.assert_match(r2)

    def test_get_package_manager(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the a LabBook's package manager dependencies"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook4", description="my first labbook10000")

        query = """
                    {
                      labbook(owner: "default", name: "labbook4") {
                        environment {
                         packageDependencies {
                            edges {
                              node {
                                id
                                schema
                                manager
                                package
                                version
                                fromBase
                              }
                              cursor
                            }
                            pageInfo {
                              hasNextPage
                            }
                          }
                        }
                      }
                    }
                    """
        # should be null
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        # Add a base image
        cm = ComponentManager(lb)
        pkgs = [{"manager": "pip", "package": "requests", "version": "1.3"},
                {"manager": "pip", "package": "numpy", "version": "1.12"}]
        cm.add_packages('pip', pkgs)

        # Add one package without a version, which should cause an error in the API since version is required
        pkgs = [{"manager": "apt", "package": "docker", "version": ""},
                {"manager": "apt", "package": "lxml", "version": "3.4"}]
        cm.add_packages('apt', pkgs)

        # Test again
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        query = """
                   {
                     labbook(owner: "default", name: "labbook4") {
                       environment {
                        packageDependencies(first: 2, after: "MA==") {
                            edges {
                              node {
                                id
                                manager
                                package
                                version
                                fromBase
                              }
                              cursor
                            }
                            pageInfo {
                              hasNextPage
                            }
                          }
                       }
                     }
                   }
                   """
        r1 = fixture_working_dir_env_repo_scoped[2].execute(query)
        assert 'errors' not in r1
        snapshot.assert_match(r1)

    def test_package_query_with_errors(self, snapshot, fixture_working_dir_env_repo_scoped):
        """Test querying for package info"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook5", description="my first labbook10000")

        query = """
                    {
                      labbook(owner: "default", name: "labbook5"){
                        id
                        packages(packageInput: [
                          {manager: "pip", package: "numpy", version:"1.14.2"},
                          {manager: "pip", package: "plotly", version:"100.00"},
                          {manager: "pip", package: "scipy", version:""},
                          {manager: "pip", package: "asdfasdfasdf", version:""}]){
                          id
                          manager 
                          package
                          version
                          isValid     
                        }
                      }
                    }
                """

        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_package_query(self, snapshot, fixture_working_dir_env_repo_scoped):
        """Test querying for package info"""
        # Create labbook
        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.new(owner={"username": "default"}, name="labbook6", description="my first labbook10000")

        query = """
                    {
                      labbook(owner: "default", name: "labbook6"){
                        id
                        packages(packageInput: [
                          {manager: "pip", package: "numpy", version:"1.14.2"},
                          {manager: "pip", package: "scipy", version:""}]){
                          id
                          manager 
                          package
                          version
                          isValid     
                        }
                      }
                    }
                """

        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

