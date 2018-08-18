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
from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped
from graphene.test import Client
from mock import patch

from lmcommon.configuration import Configuration


class TestEnvironmentCustomDependencyQueries(object):
    def test_get_available_custom_deps(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependencies"""
        query = """
               {
                  availableCustomDependencies {
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
                        osBaseClass
                        requiredPackageManagers
                        dockerSnippet
                      }
                    }
                  }
                }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_available_custom_deps_pagination(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependencies"""
        query = """
                {
                  availableCustomDependencies(first: 1) {
                    edges {
                      node {
                        id
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

        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        query = """
                {
                  availableCustomDependencies(first: 2, after: "MA==") {
                    edges {
                      node {
                        id
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

        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_available_custom_deps_pagination_reverse(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependencies using pagination from the end"""
        query = """
                {
                  availableCustomDependencies(last: 1) {
                    edges {
                      node {
                        id
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
                """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

        query = """
                {
                  availableCustomDependencies(last: 2, before: "MQ==") {
                    edges {
                      node {
                        id
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
               """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))

    def test_get_custom_deps_by_node(self, fixture_working_dir_env_repo_scoped, snapshot):
        """Test getting the available custom dependency by node ID"""
        query = """
                    {
                      node(id: "Q3VzdG9tQ29tcG9uZW50OmdpZy1kZXZfY29tcG9uZW50czImcGlsbG93JjA=") {
                        ... on CustomComponent{
                            id
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
                      }
                    }
        """
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query))
