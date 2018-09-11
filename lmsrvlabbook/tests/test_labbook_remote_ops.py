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
import responses
from lmcommon.labbook import LabBook

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir

import pytest


DUMMY_DATA = [
                {
                    "environment": {
                        "base": {
                            "name": "Python3 Minimal",
                            "os_class": "ubuntu",
                            "os_release": "18.04",
                            "languages": [
                                "python3"
                            ],
                            "development_tools": [
                                "jupyterlab"
                            ],
                            "description": "A minimal Base containing Python 3.6 and JupyterLab with no additional packages"
                        },
                        "packages": {
                            "pip": 1
                        }
                    },
                    "hashed_namespace": "26fdb6eafd356c3e4ae0303f5f39e431|tester",
                    "created_at": "2018-08-30T18:01:33.312Z",
                    "namespace": "tester",
                    "storage_size": 122,
                    "project_schema": 1,
                    "indexed_at": "2018-08-30T18:01:49.165815Z",
                    "visibility": "private_project",
                    "project": "test-proj-1",
                    "description": "No Description",
                    "modified_at": "2018-08-30T18:01:33.312Z"
                },
                {
                    "environment": {
                        "base": {
                            "name": "Python3 Minimal",
                            "os_class": "ubuntu",
                            "os_release": "18.04",
                            "languages": [
                                "python3"
                            ],
                            "development_tools": [
                                "jupyterlab"
                            ],
                            "description": "A minimal Base containing Python 3.6 and JupyterLab with no additional packages"
                        },
                        "packages": {
                            "pip": 1
                        }
                    },
                    "hashed_namespace": "26fdb6eafd356c3e4ae0303f5f39e431|tester",
                    "created_at": "2018-08-29T18:01:33.312Z",
                    "namespace": "tester",
                    "storage_size": 122,
                    "project_schema": 1,
                    "indexed_at": "2018-08-30T18:01:49.165815Z",
                    "visibility": "private_project",
                    "project": "test-proj-2",
                    "description": "No Description",
                    "modified_at": "2018-09-01T18:01:33.312Z"
                }
            ]


class TestLabBookRemoteOperations(object):

    def test_delete_remote_labbook_dryrun(self, fixture_working_dir):
        """Test deleting a LabBook on a remote server - dry run"""

        delete_query = f"""
        mutation delete {{
            deleteRemoteLabbook(input: {{
                owner: "default",
                labbookName: "new-labbook",
                confirm: false
            }}) {{
                success
            }}
        }}
        """
        r = fixture_working_dir[2].execute(delete_query)
        print(r)
        assert 'errors' not in r
        assert r['data']['deleteRemoteLabbook']['success'] is False

    @responses.activate
    def test_delete_remote_labbook(self, fixture_working_dir):
        """Test deleting a LabBook on a remote server"""
        # Setup responses mock for this test
        responses.add(responses.GET, 'https://usersrv.gigantum.io/key',
                      json={'key': 'afaketoken'}, status=200)
        responses.add(responses.GET, 'https://repo.gigantum.io/api/v4/projects/default%2Fnew-labbook',
                      json=[{
                              "id": 27,
                              "description": "",
                            }],
                      status=200)
        responses.add(responses.DELETE, 'https://repo.gigantum.io/api/v4/projects/default%2Fnew-labbook',
                      json={
                                "message": "202 Accepted"
                            },
                      status=202)
        responses.add(responses.GET, 'https://repo.gigantum.io/api/v4/projects/default%2Fnew-labbook',
                      json=[{
                                "message": "404 Project Not Found"
                            }],
                      status=404)
        responses.add(responses.DELETE, 'https://api.gigantum.com/read/index/default%2Fnew-labbook',
                      json=[{
                                "message": "success"
                            }],
                      status=204)

        delete_query = f"""
        mutation delete {{
            deleteRemoteLabbook(input: {{
                owner: "default",
                labbookName: "new-labbook",
                confirm: true
            }}) {{
                success
            }}
        }}
        """
        r = fixture_working_dir[2].execute(delete_query)
        assert 'errors' not in r
        assert r['data']['deleteRemoteLabbook']['success'] is True

        # Try deleting again, which should return an eror
        r = fixture_working_dir[2].execute(delete_query)
        assert 'errors' in r
        assert r['errors'][0]['message'] == 'Cannot remove remote repository that does not exist'

    def test_list_remote_labbooks_invalid_args(self, fixture_working_dir, snapshot):
        """test list labbooks"""
        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "asdf", sort: "desc", first: 2){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""
        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' in r
        snapshot.assert_match(r)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "name", sort: "asdf", first: 2){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""
        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' in r
        snapshot.assert_match(r)

    @responses.activate
    def test_list_remote_labbooks_az(self, fixture_working_dir, snapshot):
        """test list labbooks"""
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=2&page=1&order_by=name&sort=desc',
                      json=DUMMY_DATA, status=200)
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=2&page=1&order_by=name&sort=asc',
                      json=list(reversed(DUMMY_DATA)), status=200)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "name", sort: "desc", first: 2){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "name", sort: "asc", first: 10){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

    @responses.activate
    def test_list_remote_labbooks_modified(self, fixture_working_dir, snapshot):
        """test list labbooks"""
        """test list labbooks"""
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=2&page=1&order_by=modified_on&sort=desc',
                      json=list(reversed(DUMMY_DATA)), status=200)
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=10&page=1&order_by=modified_on&sort=asc',
                      json=DUMMY_DATA, status=200)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "modified_on", sort: "desc", first: 2){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "modified_on", sort: "asc", first: 10){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

    @responses.activate
    def test_list_remote_labbooks_created(self, fixture_working_dir, snapshot):
        """test list labbooks"""
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=2&page=1&order_by=created_on&sort=desc',
                      json=DUMMY_DATA, status=200)
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=2&page=1&order_by=created_on&sort=asc',
                      json=list(reversed(DUMMY_DATA)), status=200)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "created_on", sort: "desc", first: 2){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "created_on", sort: "asc", first: 10){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

    @responses.activate
    def test_list_remote_labbooks_page(self, fixture_working_dir, snapshot):
        """test list labbooks"""
        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=1&page=1&order_by=name&sort=desc',
                      json=[DUMMY_DATA[0]], status=200)

        responses.add(responses.GET, 'https://api.gigantum.com/read/projects?per_page=2&page=2&order_by=name&sort=desc',
                      json=[DUMMY_DATA[1]], status=200)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "name", sort: "desc", first: 1){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                            isLocal
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

        list_query = """
                    {
                    labbookList{
                      remoteLabbooks(orderBy: "name", sort: "asc", first: 2, after: "MA=="){
                        edges{
                          node{
                            id
                            description
                            creationDateUtc
                            modifiedDateUtc
                            name
                            owner
                          }
                          cursor
                        }
                        pageInfo{
                          hasNextPage
                        }
                      }
                    }
                    }"""

        r = fixture_working_dir[2].execute(list_query)
        assert 'errors' not in r
        snapshot.assert_match(r)

