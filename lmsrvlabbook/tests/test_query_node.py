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
from lmsrvlabbook.tests.fixtures import fixture_working_dir, fixture_test_file

from graphene.test import Client
import graphene
from mock import patch

from lmcommon.labbook import LabBook
from lmcommon.files import FileOperations
from lmcommon.configuration import Configuration

from ..api import LabbookMutations, LabbookQuery


class TestNodeQueries(object):

    def test_node_labbook_from_object(self, fixture_working_dir, snapshot):
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="cat-lab-book1", description="Test cat labbook from obj")

        query = """
                {
                    node(id: "TGFiYm9vazpkZWZhdWx0JmNhdC1sYWItYm9vazE=") {
                        ... on Labbook {
                            name
                            description
                            activeBranch {
                                refName
                            }
                        }
                        id
                    }
                }
                """

        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_node_package(self, fixture_working_dir, snapshot):
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="node-env-test-lb", description="Example labbook by mutation.")

        env_query = """
        {
            node(id: "UGFja2FnZUNvbXBvbmVudDpwaXAmbnVtcHkmMS4xMg==") {
                id
                ... on PackageComponent {
                    manager
                    package
                    version
                    latestVersion
                }
            }
        }
        """
        results = fixture_working_dir[2].execute(env_query)
        results['data']['node']['manager'] == 'pip'
        results['data']['node']['package'] == 'numpy'
        results['data']['node']['version'] == '1.12'
        # NOTE - The following will return None because there is no data loader available.
        #results['data']['node']['latestVersion'] == '1.14.2'

    def test_node_environment(self, fixture_working_dir, snapshot):
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="node-env-test-lb", description="Example labbook by mutation.")

        env_query = """
        {
            node(id: "TGFiYm9vazpkZWZhdWx0Jm5vZGUtZW52LXRlc3QtbGI=") {
                id
                ... on Labbook {
                    name
                    description
                    environment {
                        id
                        imageStatus
                        containerStatus
                    }
                }
            }
        }
        """
        results = fixture_working_dir[2].execute(env_query)
        snapshot.assert_match(results)

        env_id = results['data']['node']['environment']['id']

        env_node_query = """
        {
            node(id: "%s") {
                id
                ... on Environment {
                    imageStatus
                    containerStatus
                }
            }
        }
        """ % env_id
        snapshot.assert_match(fixture_working_dir[2].execute(env_node_query))

    def test_favorites_node(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")

        # Create favorites
        lb.create_favorite("code", "test1.txt", description="My file with stuff 1")

        # Test bad node that isn't a file
        query = """
                    {
                        node(id: "TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MzMzLnR4dA==") {
                            ... on LabbookFavorite {
                                id
                                key
                                description
                                isDir
                                index
                            }
                        }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Get the actual item
        query = """
                    {
                        node(id: "TGFiYm9va0Zhdm9yaXRlOmRlZmF1bHQmbGFiYm9vazEmY29kZSZ0ZXN0MS50eHQ=") {
                            ... on LabbookFavorite {
                                id
                                key
                                description
                                isDir
                                index
                            }
                        }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_file_node(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")

        # Create favorites
        lb.create_favorite("code", "test1.txt", description="My file with stuff 1")

        query = """
                    {
                        node(id: "TGFiYm9va0ZpbGU6ZGVmYXVsdCZsYWJib29rMSZjb2RlJnRlc3QxLnR4dA==") {
                            ... on LabbookFile {
                                id
                                key
                                isDir
                                size
                            }
                        }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_activity_record_node(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test getting an activity record by node ID"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my test description")
        FileOperations.insert_file(lb, "code", fixture_test_file)

        # Get activity record to
        query = """
        {
          labbook(name: "labbook1", owner: "default") {               
            activityRecords {
                edges{
                    node{
                        id
                        commit
                        linkedCommit
                        message
                        type
                        show
                        importance
                        tags
                        detailObjects{
                            id
                            key
                            type
                            data
                            show
                            importance
                            tags
                        }
                        }                        
                    }    
            }
          }
        }
        """
        result1 = fixture_working_dir[2].execute(query)

        query = """
                    {{
                        node(id: "{}") {{
                            ... on ActivityRecordObject {{
                                id
                                commit
                                linkedCommit
                                message
                                type
                                show
                                importance
                                tags
                                detailObjects{{
                                    id
                                    key
                                    type
                                    data
                                    show
                                    importance
                                    tags
                                }}     
                            }}
                        }}
                    }}
                    """.format(result1['data']['labbook']['activityRecords']['edges'][0]['node']['id'])
        result2 = fixture_working_dir[2].execute(query)
        assert result2['data']['node'] == result1['data']['labbook']['activityRecords']['edges'][0]['node']

    def test_detail_record_node(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test getting an detail record by node ID"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my test description")
        FileOperations.insert_file(lb, "code", fixture_test_file)

        # Get activity record to
        query = """
        {
          labbook(name: "labbook1", owner: "default") {               
            activityRecords {
                edges{
                    node{
                        id
                        commit
                        linkedCommit
                        message
                        type
                        show
                        importance
                        tags
                        detailObjects{
                            id
                            key
                            type
                            data
                            show
                            importance
                            tags
                        }
                        }                        
                    }    
            }
          }
        }
        """
        result1 = fixture_working_dir[2].execute(query)

        query = """
            {{
                node(id: "{}") {{
                    ... on ActivityDetailObject {{
                            id
                            key
                            type
                            data
                            show
                            importance
                            tags   
                    }}
                }}
            }}
            """.format(result1['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['id'])
        result2 = fixture_working_dir[2].execute(query)
        assert result2['data']['node'] == result1['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]
