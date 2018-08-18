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
import pytest

from snapshottest import snapshot
from lmsrvlabbook.tests.fixtures import fixture_working_dir
from lmcommon.configuration import Configuration

from graphene.test import Client
import graphene
from mock import patch


class TestUserIdentityMutations(object):
    def test_remove_user_identity(self, fixture_working_dir, snapshot):
        query = """
                {
                    userIdentity{
                                  id
                                  username
                                  email
                                  givenName
                                  familyName
                                }
                }
                """

        snapshot.assert_match(fixture_working_dir[2].execute(query))

        identity_file = os.path.join(fixture_working_dir[1], '.labmanager', 'identity', 'cached_id_jwt')
        assert os.path.exists(identity_file) is True

        query = """
                mutation myRemoveMutation {
                    removeUserIdentity(input:{}){
                    userIdentityEdge{
                      username
                    }
                  } 
                }
                """

        snapshot.assert_match(fixture_working_dir[2].execute(query))

        assert os.path.exists(identity_file) is False
