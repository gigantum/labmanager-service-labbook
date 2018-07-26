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
import io
import math
import os
import tempfile
import datetime
import pprint
from zipfile import ZipFile
from pkg_resources import resource_filename
import getpass
import responses

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import (property_mocks_fixture, docker_socket_fixture,
    fixture_working_dir_env_repo_scoped, fixture_working_dir, _create_temp_work_dir)

import pytest
from graphene.test import Client
from mock import patch
from werkzeug.datastructures import FileStorage
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request
from werkzeug.datastructures import FileStorage

from lmcommon.configuration import Configuration
from lmcommon.dispatcher.jobs import export_labbook_as_zip
from lmcommon.fixtures import remote_labbook_repo, mock_config_file
from lmcommon.labbook import LabBook
from lmcommon.files import FileOperations

@pytest.fixture()
def mock_create_labbooks(fixture_working_dir):
    # Create a labbook in the temporary directory
    lb = LabBook(fixture_working_dir[0])
    lb.new(owner={"username": "default"}, name="sample-repo-lb", description="Cats labbook 1")

    # Create a file in the dir
    with open(os.path.join(fixture_working_dir[1], 'codefile.c'), 'w') as sf:
        sf.write("1234567")
        sf.seek(0)
    FileOperations.insert_file(lb, 'code', sf.name)

    assert os.path.isfile(os.path.join(lb.root_dir, 'code', 'codefile.c'))
    # name of the config file, temporary working directory, the schema
    yield fixture_working_dir, lb


class TestLabbookSharing(object):

    @responses.activate
    def test_import_remote_labbook(self, remote_labbook_repo, fixture_working_dir, property_mocks_fixture,
                                   docker_socket_fixture):

        # Mock the request context so a fake authorization header is present
        builder = EnvironBuilder(path='/labbook', method='POST', headers={'Authorization': 'Bearer AJDFHASD'})
        env = builder.get_environ()
        req = Request(environ=env)

        query = f"""
        mutation importFromRemote {{
          importRemoteLabbook(
            input: {{
              owner: "test",
              labbookName: "sample-repo-lb",
              remoteUrl: "{remote_labbook_repo}"
            }}) {{
                newLabbookEdge {{
                    node {{
                        owner
                        name
                    }}
                }}
            }}
        }}
        """
        r = fixture_working_dir[2].execute(query, context_value=req)
        pprint.pprint(r)
        # Note this is testing cloning a PUBLIC labbook so the owner should get changed.
        assert r['data']['importRemoteLabbook']['newLabbookEdge']['node']['owner'] == 'default'
        assert r['data']['importRemoteLabbook']['newLabbookEdge']['node']['name'] == 'sample-repo-lb'
        assert 'errors' not in r

        new_owner = r['data']['importRemoteLabbook']['newLabbookEdge']['node']['owner']

        ## Now we want to validate that when we import a labbook from a remote url, we also track the default branch.
        list_all_branches_q = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "{new_owner}") {{
                branches {{
                    edges {{
                        node {{
                            prefix
                            refName
                        }}
                    }}
                }}
            }}
        }}
        """
        r = fixture_working_dir[2].execute(list_all_branches_q, context_value=req)
        pprint.pprint(r)
        nodes = r['data']['labbook']['branches']['edges']
        for n in [x['node'] for x in nodes]:
            # Make sure that the user's local branch was created
            if n['prefix'] is None and n['refName'] == f'gm.workspace-{new_owner}':
                break
        else:
            assert False, f"Branch gm.workspace-{new_owner} should exist but does not"

        for n in [x['node'] for x in nodes]:
            # Make sure that origin/gm.workspace is in list of branches. This means it tracks.
            if n['refName'] == 'gm.workspace':
                break
        else:
            pprint.pprint(nodes)
            assert False, "gm.workspace should be in list of branches"

        # Make sure the labbook cloned into the correct directory
        assert os.path.exists(os.path.join(fixture_working_dir[1], 'default', new_owner, 'labbooks', 'sample-repo-lb'))

        # Now do a quick test for default_remote
        get_default_remote_q = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "{new_owner}") {{
                defaultRemote
            }}
        }}
        """
        r = fixture_working_dir[2].execute(get_default_remote_q, context_value=req)
        #assert r['data']['labbook']['defaultRemote'] == remote_labbook_repo
        assert 'errors' not in r

    def test_import_remote_labbook_from_same_user(self, remote_labbook_repo, fixture_working_dir):
        # Create a labbook by the "default" user
        # TODO: enable LFS when integration tests support it
        conf_file, working_dir = _create_temp_work_dir(lfs_enabled=False)
        lb = LabBook(conf_file)
        labbook_dir = lb.new(username="default", name="default-owned-repo-lb", description="my first labbook",
                             owner={"username": "default"})
        lb.checkout_branch("gm.workspace")

        # Mock the request context so a fake authorization header is present
        builder = EnvironBuilder(path='/labbook', method='POST', headers={'Authorization': 'Bearer AJDFHASD'})
        env = builder.get_environ()
        req = Request(environ=env)

        query = f"""
        mutation importFromRemote {{
          importRemoteLabbook(
            input: {{
              owner: "default",
              labbookName: "default-owned-repo-lb",
              remoteUrl: "{labbook_dir}"
            }}) {{
                newLabbookEdge {{
                    node {{
                        owner
                        name
                    }}
                }}
            }}
        }}
        """
        r = fixture_working_dir[2].execute(query, context_value=req)
        pprint.pprint(r)
        assert 'errors' not in r
        # We might not always want to use master as the default branch, but keep it here for now.
        assert r['data']['importRemoteLabbook']['newLabbookEdge']['node']['owner'] == 'default'
        assert r['data']['importRemoteLabbook']['newLabbookEdge']['node']['name'] == 'default-owned-repo-lb'

        ## Now we want to validate that when we import a labbook from a remote url, we also track the default branch.
        list_all_branches_q = f"""
        {{
            labbook(name: "default-owned-repo-lb", owner: "default") {{
                branches {{
                    edges {{
                        node {{
                            prefix
                            refName
                        }}
                    }}
                }}
            }}
        }}
        """
        r = fixture_working_dir[2].execute(list_all_branches_q, context_value=req)
        pprint.pprint(r)
        nodes = r['data']['labbook']['branches']['edges']
        assert 'errors' not in r
        for n in [x['node'] for x in nodes]:
            # Make sure that origin/master is in list of branches. This means it tracks.
            if n['prefix'] == 'origin' and n['refName'] == 'gm.workspace':
                break
        else:
            pprint.pprint(nodes)
            assert False, "Did not check out gm.workspace branch"

        # Make sure the labbook cloned into the correct directory
        assert os.path.exists(os.path.join(fixture_working_dir[1], 'default', 'default', 'labbooks',
                                           'default-owned-repo-lb'))

        # Now do a quick test for default_remote
        get_default_remote_q = f"""
        {{
            labbook(name: "default-owned-repo-lb", owner: "default") {{
                defaultRemote
            }}
        }}
        """
        r = fixture_working_dir[2].execute(get_default_remote_q, context_value=req)
        assert r['data']['labbook']['defaultRemote'] == labbook_dir
        assert 'errors' not in r

    def test_can_checkout_branch(self, mock_create_labbooks, remote_labbook_repo, fixture_working_dir):
        """Test whether there are uncommitted changes or anything that would prevent
        having a fresh branch checked out. """

        f_dir, lb = mock_create_labbooks

        query = f"""
        {{
            labbook(name: "sample-repo-lb", owner: "default") {{
                isRepoClean
            }}
        }}
        """
        r = fixture_working_dir[2].execute(query)
        assert r['data']['labbook']['isRepoClean'] is True

        os.remove(os.path.join(lb.root_dir, 'code', 'codefile.c'))

        r = fixture_working_dir[2].execute(query)
        # We back-door deleted a file in the LB. The repo should now be unclean - prove it.
        assert r['data']['labbook']['isRepoClean'] is False
