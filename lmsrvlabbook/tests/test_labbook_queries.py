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
from lmcommon.files import FileOperations
from lmcommon.fixtures import ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_BASE, ENV_UNIT_TEST_REV
import datetime
import pprint

import graphene

import lmcommon
from lmcommon.labbook import LabBook
from lmcommon.fixtures import remote_labbook_repo
from lmcommon.gitlib.git import GitAuthor


class TestLabBookServiceQueries(object):
    def test_pagination_noargs(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_sort_az(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks(orderBy: "name") {
                        edges {
                            node {
                                id
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_sort_az_reverse(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks(orderBy: "name", sort: "desc") {
                        edges {
                            node {
                                id
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_sort_create(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks(orderBy: "created_on") {
                        edges {
                            node {
                                id
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_sort_modified(self, fixture_working_dir_populated_scoped, snapshot):

        query = """
                {
                labbookList{
                    localLabbooks(orderBy: "modified_on") {
                        edges {
                            node {
                                id
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

        # Modify a labbook
        lb = LabBook()
        lb.from_name("default", "default", "labbook4")
        with open(os.path.join(lb.root_dir, "code", "test.txt"), 'wt') as tf:
            tf.write("asdfasdf")
        lb.git.add_all()
        lb.git.commit("Changing the repo")

        # Run query again
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_first_only(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks(first: 3) {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_first_and_after(self, fixture_working_dir_populated_scoped, snapshot):
        # Nominal case
        query = """
                {
                labbookList{
                    localLabbooks(first: 4, after: "Mg==") {
                        edges {
                            node {
                                name
                                description
                            }
                            cursor
                        }
                        pageInfo {
                            hasNextPage
                            hasPreviousPage
                            startCursor
                            endCursor
                        }
                    }
                }
                }
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

        # Overrunning end of list of labbooks
        query = """
                {
                labbookList{
                    localLabbooks(first: 6, after: "Ng==") {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

        # Overrunning end of list of labbooks, returns empty set.
        query = """
                {
                labbookList{
                    localLabbooks(first: 6, after: "OA==") {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_last_only(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks(last: 3) {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination_last_and_before(self, fixture_working_dir_populated_scoped, snapshot):
        query = """
                {
                labbookList{
                    localLabbooks(last: 3, before: "Nw==") {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

        # Overrun start of list
        query = """
                {
                labbookList{
                    localLabbooks(last: 3, before: "MQ==") {
                        edges {
                            node {
                                name
                                description
                            }
                            cursor
                        }
                        pageInfo {
                            hasNextPage
                            hasPreviousPage
                            startCursor
                            endCursor
                        }
                    }
                }
                }
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

        # Overrun with no intersection (should return empty list)
        query = """
                {
                labbookList{
                    localLabbooks(last: 3, before: "MA==") {
                        edges {
                            node {
                                name
                                description
                            }
                            cursor
                        }
                        pageInfo {
                            hasNextPage
                            hasPreviousPage
                            startCursor
                            endCursor
                        }
                    }
                }
                }
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

    def test_pagination(self, fixture_working_dir_populated_scoped, snapshot):
        """Test pagination and cursors"""
        # Get LabBooks for the "logged in user" - Currently just "default"
        query = """
                {
                labbookList{
                    localLabbooks(first: 2, after: "MQ==") {
                        edges {
                            node {
                                name
                                description
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
                """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(query))

        before_query = """
                    {
                    labbookList{
                        localLabbooks(last: 2, before: "Ng==") {
                            edges {
                                node {
                                    name
                                    description
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
                    """
        snapshot.assert_match(fixture_working_dir_populated_scoped[2].execute(before_query))

    def test_labbook_schema_version(self, fixture_working_dir):
        # Get LabBooks for the "logged in user" - Currently just "default"
        query = """
        {
            currentLabbookSchemaVersion
        }
        """
        r = fixture_working_dir[2].execute(query)
        assert 'errors' not in r
        assert r['data']['currentLabbookSchemaVersion'] == 1

    def test_get_labbook(self, fixture_working_dir):
        """Test listing labbooks"""
        # Create labbooks
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Get LabBooks for a single user - Don't get the ID field since it is a UUID
        query = """
        {
          labbook(name: "labbook1", owner: "default") {
            schemaVersion
            name
            sizeBytes
            description
            creationDateUtc
            activeBranch {
                refName
                prefix
            }
          }
        }
        """
        r = fixture_working_dir[2].execute(query)
        assert 'errors' not in r
        assert r['data']['labbook']['schemaVersion'] == 1
        assert int(r['data']['labbook']['sizeBytes']) > 10000
        assert int(r['data']['labbook']['sizeBytes']) < 40000
        assert r['data']['labbook']['activeBranch']['refName'] == 'gm.workspace-default'
        assert r['data']['labbook']['activeBranch']['prefix'] is None
        assert r['data']['labbook']['name'] == 'labbook1'
        d = r['data']['labbook']['creationDateUtc']
        n = datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%f')
        assert (datetime.datetime.utcnow() - n).total_seconds() < 30

    def test_get_labbook_size_rediculously_huge(self, monkeypatch, fixture_working_dir):
        """Test listing labbooks"""
        # Create labbooks
        monkeypatch.setattr(lmcommon.files.FileOperations, 'content_size', lambda labbook: (2**32)*34)
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="unittest-labbook1", description="my first labbook1")

        # Get LabBooks for a single user - Don't get the ID field since it is a UUID
        query = """
        {
          labbook(name: "unittest-labbook1", owner: "default") {
            sizeBytes
          }
        }
        """
        r = fixture_working_dir[2].execute(query)
        assert 'errors' not in r
        assert int(r['data']['labbook']['sizeBytes']) == (2**32)*34

    def test_list_labbooks_container_status(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "test3"}, name="labbook2", description="my first labbook3")

        # Get LabBooks for the "logged in user" - Currently just "default"
        query = """
        {
        labbookList{
            localLabbooks {
                edges {
                    node {
                        name
                        description
                        environment{
                            imageStatus
                            containerStatus
                        }
                    }
                    cursor
                }
            }
        }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_list_local_by_id(self, fixture_working_dir, snapshot):
        """Test listing labbooks"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")
        lb.new(owner={"username": "default"}, name="labbook2", description="my first labbook2")
        lb.new(owner={"username": "default"}, name="labbook3", description="my first labbook3")

        query = """
        {
        labbookList{
            localLabbooks {
                edges {
                    node {
                       id
                    }                    
                }
            }
        }
        }
        """
        result1 = fixture_working_dir[2].execute(query)

        query = """
               {
               labbookList{
                   localById(ids: ["TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sx", "TGFiYm9vazpkZWZhdWx0JmxhYmJvb2sz", "notanid"]){
                      id
                      name
                      owner
                      description
                    }
                 }
               }
               """
        result2 = fixture_working_dir[2].execute(query)
        snapshot.assert_match(result2)

        assert result1['data']['labbookList']['localLabbooks']['edges'][0]['node']['id'] == result2['data']['labbookList']['localById'][0]['id']
        assert result1['data']['labbookList']['localLabbooks']['edges'][2]['node']['id'] == result2['data']['labbookList']['localById'][1]['id']

    def test_list_labbooks_container_status_no_labbooks(self, fixture_working_dir, snapshot):
        """Test listing labbooks when none exist"""
        # Get LabBooks for the "logged in user" - Currently just "default"
        query = """
        {
        labbookList{
            localLabbooks {
                edges {
                    node {
                        name
                        description
                        environment{
                            imageStatus
                            containerStatus
                        }
                    }
                    cursor
                }
            }
        }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_list_files_code(self, fixture_working_dir, snapshot):
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Write data in code
        with open(os.path.join(lb.root_dir, 'code', "test_file1.txt"), 'wt') as tf:
            tf.write("file 1")
        with open(os.path.join(lb.root_dir, 'code', "test_file2.txt"), 'wt') as tf:
            tf.write("file 2!!!!!!!!!")
        with open(os.path.join(lb.root_dir, 'code', ".hidden_file.txt"), 'wt') as tf:
            tf.write("Should be hidden")

        # Create subdirs and data
        os.makedirs(os.path.join(lb.root_dir, 'code', 'src', 'js'))
        with open(os.path.join(lb.root_dir, 'code', 'src', 'test.py'), 'wt') as tf:
            tf.write("print('hello, world')")
        with open(os.path.join(lb.root_dir, 'code', 'src', 'js', 'test.js'), 'wt') as tf:
            tf.write("asdfasdf")

        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Just get the files in the sub-directory "js"
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            files(rootDir: "src") {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Just get the files in the sub-directory "js"
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            files(rootDir: "src/") {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_list_files_many(self, fixture_working_dir, snapshot):
        # Add some extra files for listing
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Write data in code
        with open(os.path.join(lb.root_dir, 'code', "test_file1.txt"), 'wt') as tf:
            tf.write("file 1")
        with open(os.path.join(lb.root_dir, 'code', "test_file2.txt"), 'wt') as tf:
            tf.write("file 2!!!!!!!!!")
        with open(os.path.join(lb.root_dir, 'code', ".hidden_file.txt"), 'wt') as tf:
            tf.write("Should be hidden")

        # Create subdirs and data
        os.makedirs(os.path.join(lb.root_dir, 'input', 'subdir', 'data'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'empty'))
        with open(os.path.join(lb.root_dir, 'input', 'subdir', 'data.dat'), 'wt') as tf:
            tf.write("adsfasdfasdf")
        with open(os.path.join(lb.root_dir, 'output', 'result.dat'), 'wt') as tf:
            tf.write("fgh")

        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                        input{
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                        output{
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Just get the files in the sub-directory "js"
        query = """
                {
                  labbook(name: "labbook1", owner: "default") {
                    name
                    code{
                        files {
                            edges {
                                node {
                                    id
                                    key
                                    size
                                    isDir
                                }
                            }
                        }
                    }
                    input{
                        files(rootDir: "subdir") {
                            edges {
                                node {
                                    id
                                    key
                                    size
                                    isDir
                                }
                            }
                        }
                    }
                    output{
                        files(rootDir: "empty") {
                            edges {
                                node {
                                    id
                                    key
                                    size
                                    isDir
                                }
                            }
                        }
                    }
                  }
                }
                """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_check_updates_available_from_remote(self, remote_labbook_repo, fixture_working_dir, snapshot):
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        query = f"""
        {{
            labbook(name: "labbook1", owner: "default") {{
                updatesAvailableCount
            }}
        }}
        """
        r = fixture_working_dir[2].execute(query)
        assert r['data']['labbook']['updatesAvailableCount'] == 0

    def test_list_favorites(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")
        with open(os.path.join(lb.root_dir, 'code', 'test2.txt'), 'wt') as test_file:
            test_file.write("blah2")

        # Setup a favorite dir in input
        os.makedirs(os.path.join(lb.root_dir, 'code', 'blah'))
        os.makedirs(os.path.join(lb.root_dir, 'input', 'data1'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'data2'))

        # Create favorites
        lb.create_favorite("code", "test1.txt", description="My file with stuff 1")
        lb.create_favorite("code", "test2.txt", description="My file with stuff 2")
        lb.create_favorite("code", "blah/", description="testing", is_dir=True)
        lb.create_favorite("input", "data1/", description="Data dir 1", is_dir=True)
        lb.create_favorite("output", "data2/", description="Data dir 2", is_dir=True)

        # Get LabBooks for the "logged in user" - Currently just "default"
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Get input favorites
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        input{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Get output favorites
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        output{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Get all favorites
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                }
                            }
                        }
                        input{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                }
                            }
                        }
                        output{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_page_favorites(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""

        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")
        with open(os.path.join(lb.root_dir, 'code', 'test2.txt'), 'wt') as test_file:
            test_file.write("blah2")

        # Setup a favorite dir in input
        os.makedirs(os.path.join(lb.root_dir, 'code', 'blah'))
        os.makedirs(os.path.join(lb.root_dir, 'input', 'data1'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'data2'))

        # Create favorites
        lb.create_favorite("code", "test1.txt", description="My file with stuff 1")
        lb.create_favorite("code", "test2.txt", description="My file with stuff 2")
        lb.create_favorite("code", "blah/", description="testing", is_dir=True)
        lb.create_favorite("input", "data1/", description="Data dir 1", is_dir=True)
        lb.create_favorite("output", "data2/", description="Data dir 2", is_dir=True)

        # Get 2 only
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            favorites(first: 2){
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                    cursor
                                }                                                   
                                pageInfo{
                                    startCursor
                                    hasNextPage
                                    hasPreviousPage
                                    endCursor
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Get last page
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            favorites(first: 2, after: "MQ=="){
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                        associatedLabbookFileId
                                    }
                                    cursor
                                }                                                   
                                pageInfo{
                                    startCursor
                                    hasNextPage
                                    hasPreviousPage
                                    endCursor
                                }
                            }
                        }
                      }
                    }
                    """

        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_list_favorite_and_files(self, fixture_working_dir, snapshot):
        """Test listing labbook favorites"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Setup some favorites in code
        with open(os.path.join(lb.root_dir, 'code', 'test1.txt'), 'wt') as test_file:
            test_file.write("blah1")
        with open(os.path.join(lb.root_dir, 'code', 'test2.txt'), 'wt') as test_file:
            test_file.write("blah2")

        # Setup a favorite dir in input
        os.makedirs(os.path.join(lb.root_dir, 'code', 'blah'))

        # Create favorites
        lb.create_favorite("code", "test2.txt", description="My file with stuff 2")
        lb.create_favorite("code", "blah/", description="testing", is_dir=True)

        # Get LabBooks for the "logged in user" - Currently just "default"
        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            favorites{
                                edges {
                                    node {
                                        id
                                        index
                                        key
                                        description
                                        isDir
                                    }
                                }
                            }                                
                            files {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_list_all_files_many(self, fixture_working_dir, snapshot):
        # Add some extra files for listing
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        # Write data in code
        with open(os.path.join(lb.root_dir, 'code', "test_file1.txt"), 'wt') as tf:
            tf.write("file 1")
        with open(os.path.join(lb.root_dir, 'code', "test_file2.txt"), 'wt') as tf:
            tf.write("file 2!!!!!!!!!")
        with open(os.path.join(lb.root_dir, 'code', ".hidden_file.txt"), 'wt') as tf:
            tf.write("Should be hidden")

        # Create subdirs and data
        os.makedirs(os.path.join(lb.root_dir, 'input', 'subdir', 'data'))
        os.makedirs(os.path.join(lb.root_dir, 'output', 'empty'))
        with open(os.path.join(lb.root_dir, 'input', 'subdir', 'data.dat'), 'wt') as tf:
            tf.write("adsfasdfasdf")
        with open(os.path.join(lb.root_dir, 'output', 'result.dat'), 'wt') as tf:
            tf.write("fgh")

        query = """
                    {
                      labbook(name: "labbook1", owner: "default") {
                        name
                        code{
                            allFiles {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                        input{
                            allFiles {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                        output{
                            allFiles {
                                edges {
                                    node {
                                        id
                                        key
                                        size
                                        isDir
                                    }
                                }
                            }
                        }
                      }
                    }
                    """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_activity_records_next_page(self, fixture_working_dir_env_repo_scoped, snapshot, fixture_test_file):
        """Test next page logic, which requires a labbook to be created properly with an activity"""
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
        variables = {"name": "labbook-page-test", "desc": "my test 1",
                     "component_id": ENV_UNIT_TEST_BASE, "repository": ENV_UNIT_TEST_REPO,
                     "revision": ENV_UNIT_TEST_REV}
        snapshot.assert_match(fixture_working_dir_env_repo_scoped[2].execute(query, variable_values=variables))

        lb = LabBook(fixture_working_dir_env_repo_scoped[0])
        lb.from_name("default","default", "labbook-page-test")
        FileOperations.insert_file(lb, "code", fixture_test_file)

        # Get all records at once with no pagination args and verify cursors look OK directly
        query = """
        {
          labbook(name: "labbook-page-test", owner: "default") {
            name
            description
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
                        timestamp
                        }
                    cursor
                    }                    
                pageInfo{
                    startCursor
                    hasNextPage
                    hasPreviousPage
                    endCursor
                }
            }
          }
        }
        """
        result = fixture_working_dir_env_repo_scoped[2].execute(query)

        # Check cursors
        assert result['data']['labbook']['activityRecords']['pageInfo']['hasNextPage'] is False
        assert result['data']['labbook']['activityRecords']['pageInfo']['hasPreviousPage'] is False
        assert result['data']['labbook']['activityRecords']['edges'][-1]['node']['type'] == 'LABBOOK'

    def test_get_activity_records(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test paging through activity records"""
        lb = LabBook(fixture_working_dir[0], author=GitAuthor(name="tester", email="tester@test.com"))
        lb.new(owner={"username": "default"}, name="labbook11", description="my test description")
        open('/tmp/test_file.txt', 'w').write("xxxx")
        FileOperations.insert_file(lb, "code", '/tmp/test_file.txt')
        open('/tmp/test_file.txt', 'w').write("xxxx")
        FileOperations.insert_file(lb, "input", '/tmp/test_file.txt')
        open('/tmp/test_file.txt', 'w').write("xxxx")
        FileOperations.insert_file(lb, "output", '/tmp/test_file.txt')

        # Get all records at once with no pagination args and verify cursors look OK directly
        query = """
        {
          labbook(name: "labbook11", owner: "default") {
            name
            description
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
                        timestamp
                        }
                    cursor
                    }                    
                pageInfo{
                    startCursor
                    endCursor
                }
            }
          }
        }
        """
        result = fixture_working_dir[2].execute(query)

        # Check cursors
        git_log = lb.git.log()
        assert result['data']['labbook']['activityRecords']['edges'][0]['cursor'] == git_log[0]['commit']
        assert result['data']['labbook']['activityRecords']['edges'][1]['cursor'] == git_log[2]['commit']
        assert result['data']['labbook']['activityRecords']['edges'][2]['cursor'] == git_log[4]['commit']

        assert result['data']['labbook']['activityRecords']['edges'][0]['node']['commit'] == git_log[0]['commit']
        assert result['data']['labbook']['activityRecords']['edges'][0]['node']['linkedCommit'] == git_log[1]['commit']

        # test timestamp field
        assert type(result['data']['labbook']['activityRecords']['edges'][0]['node']['timestamp']) == str
        assert result['data']['labbook']['activityRecords']['edges'][0]['node']['timestamp'][:2] == "20"

        assert type(result['data']['labbook']['activityRecords']['edges'][0]['node']['id']) == str
        assert len(result['data']['labbook']['activityRecords']['edges'][0]['node']['id']) > 0

        assert type(result['data']['labbook']['activityRecords']['pageInfo']['endCursor']) == str
        assert len(result['data']['labbook']['activityRecords']['pageInfo']['endCursor']) == 40

        # Get only the first record, verifying pageInfo and result via snapshot
        query = """
        {
          labbook(name: "labbook11", owner: "default") {
            name
            description
            activityRecords(first: 1) {
                edges{
                    node{                            
                        message
                        type
                        show
                        importance
                        tags
                        }                        
                    }                    
                pageInfo{
                    hasNextPage
                    hasPreviousPage
                }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Page 1 time
        query = """
        {{
          labbook(name: "labbook11", owner: "default") {{
            name
            description
            activityRecords(first: 2, after: "{}") {{
                edges{{
                    node{{                            
                        message
                        type
                        show
                        importance
                        tags
                        username
                        email
                        }}                        
                    }}                    
                pageInfo{{
                    hasNextPage
                    hasPreviousPage
                }}
            }}
          }}
        }}
        """.format(result['data']['labbook']['activityRecords']['edges'][0]['cursor'])
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Page past end, expecting only the last result to come back
        query = """
        {{
          labbook(name: "labbook11", owner: "default") {{
            name
            description
            activityRecords(first: 5, after: "{}") {{
                edges{{
                    node{{                            
                        message
                        type
                        show
                        importance
                        tags
                        }}                        
                    }}                    
                pageInfo{{
                    hasNextPage
                    hasPreviousPage
                }}
            }}
          }}
        }}
        """.format(result['data']['labbook']['activityRecords']['edges'][1]['cursor'])
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        # Page after end, expecting nothing to come back
        query = """
        {{
          labbook(name: "labbook11", owner: "default") {{
            name
            description
            activityRecords(first: 5, after: "{}") {{
                edges{{
                    node{{                            
                        message
                        type
                        show
                        importance
                        tags
                        }}                        
                    }}                    
                pageInfo{{
                    hasNextPage
                    hasPreviousPage
                }}
            }}
          }}
        }}
        """.format(result['data']['labbook']['activityRecords']['edges'][2]['cursor'])
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_activity_records_reverse_error(self, fixture_working_dir, snapshot):
        # Create labbooks
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook12", description="my first labbook1")

        # Get all records
        query = """
        {
          labbook(name: "labbook12", owner: "default") {
            name
            description
            activityRecords(before: "asdfasdf") {
                edges{
                    node{                            
                        message
                        type
                        show
                        importance
                        tags
                        }                        
                    }                    
                pageInfo{
                    hasNextPage
                    hasPreviousPage
                }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        query = """
        {
          labbook(name: "labbook12", owner: "default") {
            name
            description
            activityRecords(before: "asdfasdf", last: 3){
                edges{
                    node{                            
                        message
                        type
                        show
                        importance
                        tags
                        }                        
                    }                    
                pageInfo{
                    hasNextPage
                    hasPreviousPage
                }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        query = """
        {
          labbook(name: "labbook12", owner: "default") {
            name
            description
            activityRecords(last: 3) {
                edges{
                    node{                            
                        message
                        type
                        show
                        importance
                        tags
                        }                        
                    }                    
                pageInfo{
                    hasNextPage
                    hasPreviousPage
                }
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_activity_records_with_details(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test getting activity records with detail records"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook11", description="my test description")
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "code", '/tmp/test_file.txt')
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "input", '/tmp/test_file.txt')
        open('/tmp/test_file.txt', 'w').write("xxx" * 50)
        FileOperations.insert_file(lb, "output", '/tmp/test_file.txt')

        # Get all records at once and verify varying fields exist properly
        query = """
        {
          labbook(name: "labbook11", owner: "default") {
            name
            description
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
                            action
                        }
                        }                        
                    }    
            }
          }
        }
        """
        result = fixture_working_dir[2].execute(query)

        # Check ids and keys
        assert len(result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['id']) > 0
        assert type(result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['id']) == str
        assert len(result['data']['labbook']['activityRecords']['edges'][1]['node']['detailObjects'][0]['id']) > 0
        assert type(result['data']['labbook']['activityRecords']['edges'][1]['node']['detailObjects'][0]['id']) == str

        # Verify again using snapshot and only fields that will snapshot well
        query = """
        {
          labbook(name: "labbook11", owner: "default") {
            name
            description
            activityRecords {
                edges{
                    node{
                        message
                        type
                        show
                        importance
                        tags
                        detailObjects{
                            type
                            data
                            show
                            importance
                            tags
                            action
                        }
                        }                        
                    }    
            }
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_detail_record(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test getting detail record directly after an initial activity record query"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook11", description="my test description")
        FileOperations.insert_file(lb, "code", fixture_test_file)

        # Get all records at once and verify varying fields exist properly
        query = """
        {
          labbook(name: "labbook11", owner: "default") {
            name
            description
            activityRecords(first: 2) {
                edges{
                    node{
                        detailObjects{
                            id
                            key
                            type                                
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
        activity_result = fixture_working_dir[2].execute(query)

        # Load detail record based on the key you got back and verify key/id
        query = """
        {{
          labbook(name: "labbook11", owner: "default") {{
            name
            description
            detailRecord(key: "{}") {{
                id
                key
                type                                
                show
                importance
                tags 
                action
            }}
          }}
        }}
        """.format(activity_result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['key'])
        detail_result = fixture_working_dir[2].execute(query)
        assert detail_result['data']['labbook']['detailRecord']['key'] == \
               activity_result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['key']
        assert detail_result['data']['labbook']['detailRecord']['id'] == \
               activity_result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['id']
        assert detail_result['data']['labbook']['detailRecord']['action'] == "CREATE"

        # Try again in a snapshot compatible way, loading data as well
        query = """
        {{
          labbook(name: "labbook11", owner: "default") {{
            name
            description
            detailRecord(key: "{}") {{
                type                                
                show
                data
                importance
                tags 
            }}
          }}
        }}
        """.format(activity_result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['key'])
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_detail_records(self, fixture_working_dir, snapshot, fixture_test_file):
        """Test getting multiple detail records directly after an initial activity record query"""
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook11", description="my test description")
        open('/tmp/test_file.txt', 'w').write("xxxx")
        FileOperations.insert_file(lb, "code", '/tmp/test_file.txt')
        open('/tmp/test_file.txt', 'w').write("xxxx")
        FileOperations.insert_file(lb, "input", '/tmp/test_file.txt')

        # Get all records at once and verify varying fields exist properly
        query = """
        {
          labbook(name: "labbook11", owner: "default") {
            name
            description
            activityRecords(first: 2) {
                edges{
                    node{
                        detailObjects{
                            id
                            key
                            type                                
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
        activity_result = fixture_working_dir[2].execute(query)

        # create key list
        keys = [activity_result['data']['labbook']['activityRecords']['edges'][1]['node']['detailObjects'][0]['key'],
                activity_result['data']['labbook']['activityRecords']['edges'][0]['node']['detailObjects'][0]['key']]

        # Try again in a snapshot compatible way, loading data as well
        query = """
        {{
          labbook(name: "labbook11", owner: "default") {{
            name
            description
            detailRecords(keys: [{}]) {{
                type                                
                show
                data
                importance
                tags 
            }}
          }}
        }}
        """.format(",".join(f'"{k}"' for k in keys))
        snapshot.assert_match(fixture_working_dir[2].execute(query))

    def test_get_labbook_readme(self, fixture_working_dir, snapshot):
        """Test getting a labbook's readme document"""
        # Create labbooks
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="labbook1", description="my first labbook1")

        query = """
        {
          labbook(name: "labbook1", owner: "default") {
            name
            description
            readme
          }
        }
        """
        snapshot.assert_match(fixture_working_dir[2].execute(query))

        lb.write_readme("##Summary\nThis is my readme!!")

        snapshot.assert_match(fixture_working_dir[2].execute(query))
