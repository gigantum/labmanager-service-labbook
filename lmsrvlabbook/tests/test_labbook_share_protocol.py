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
import os
import responses

from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir, \
    fixture_working_dir_lfs_disabled

import pytest
from mock import patch
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from lmcommon.fixtures import (remote_labbook_repo, remote_bare_repo, mock_labbook,
                               mock_config_file, _MOCK_create_remote_repo2)
from lmcommon.labbook import LabBook, loaders
from lmcommon.workflows import GitWorkflow
from lmcommon.files import FileOperations

@pytest.fixture()
def mock_create_labbooks(fixture_working_dir):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir[0])
    lb.new(owner={"username": "default"}, name="labbook1", description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir[1], 'sillyfile'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    FileOperations.insert_file(lb, 'code', sf.name)

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'sillyfile'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir

@pytest.fixture()
def mock_create_labbooks_no_lfs(fixture_working_dir_lfs_disabled):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir_lfs_disabled[0])
    lb.new(owner={"username": "default"}, name="labbook1", description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir_lfs_disabled[1], 'sillyfile'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    FileOperations.insert_file(lb, 'code', sf.name)

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'sillyfile'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir_lfs_disabled


class TestLabbookShareProtocol(object):
    @patch('lmcommon.workflows.core.create_remote_gitlab_repo', new=_MOCK_create_remote_repo2)
    def test_publish_basic(self, fixture_working_dir, remote_bare_repo, mock_create_labbooks_no_lfs):

        # Mock the request context so a fake authorization header is present
        builder = EnvironBuilder(path='/labbook', method='POST', headers={'Authorization': 'Bearer AJDFHASD'})
        env = builder.get_environ()
        req = Request(environ=env)

        test_user_lb = LabBook(mock_create_labbooks_no_lfs[0])
        test_user_lb.from_name('default', 'default', 'labbook1')

        publish_query = f"""
        mutation c {{
            publishLabbook(input: {{
                labbookName: "labbook1",
                owner: "default"
            }}) {{
                jobKey
            }}
        }}
        """

        r = mock_create_labbooks_no_lfs[2].execute(publish_query, context_value=req)
        assert 'errors' not in r
        # TODO - Pause and wait for bg job to finish
        #assert r['data']['publishLabbook']['success'] is True

    @responses.activate
    @patch('lmcommon.workflows.core.create_remote_gitlab_repo', new=_MOCK_create_remote_repo2)
    def test_sync_1(self, remote_bare_repo, mock_create_labbooks_no_lfs, mock_config_file):

        # Setup responses mock for this test
        responses.add(responses.GET, 'https://usersrv.gigantum.io/key',
                      json={'key': 'afaketoken'}, status=200)

        test_user_lb = LabBook(mock_create_labbooks_no_lfs[0])
        test_user_lb.from_name('default', 'default', 'labbook1')
        test_user_wf = GitWorkflow(test_user_lb)
        test_user_wf.publish('default')

        # Mock the request context so a fake authorization header is present
        builder = EnvironBuilder(path='/labbook', method='POST', headers={'Authorization': 'Bearer AJDFHASD'})
        env = builder.get_environ()
        req = Request(environ=env)

        remote_url = test_user_lb.root_dir
        assert remote_url

        sally_lb = LabBook(mock_config_file[0])
        loaders.from_remote(remote_url, username="sally", owner="default", labbook_name="labbook1", labbook=sally_lb)
        sally_wf = GitWorkflow(sally_lb)
        assert sally_lb.active_branch == "gm.workspace-sally"
        FileOperations.makedir(sally_lb, relative_path='code/sally-dir', create_activity_record=True)
        sally_wf.sync('sally')

        sync_query = """
        mutation x {
            syncLabbook(input: {
                labbookName: "labbook1",
                owner: "default"
            }) {
                jobKey
            }
        }
        """
        r = mock_create_labbooks_no_lfs[2].execute(sync_query, context_value=req)

        assert 'errors' not in r
        assert test_user_lb.active_branch == 'gm.workspace-default'
        # TODO - Pause and wait for job to report finished
 
