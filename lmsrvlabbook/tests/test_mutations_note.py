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
from lmsrvlabbook.tests.fixtures import fixture_working_dir

from graphene.test import Client
import graphene
from mock import patch

from lmcommon.configuration import Configuration
from lmcommon.labbook import LabBook


class TestNoteService(object):
    def test_create_user_note_no_body(self, fixture_working_dir, snapshot):
        """Test creating and getting a user note"""
        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="user-note-test", description="testing user notes")

        # Create a user note
        query = """
        mutation makeUserNote {
          createUserNote(input: {
            owner: "default",
            labbookName: "user-note-test",
            title: "I think this is a thing"
          })
          {
            newActivityRecordEdge {
              node{
                message
                detailObjects{                
                  data
                  type
                  show
                  importance
                  tags
                }
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

    def test_create_user_note_full(self, fixture_working_dir, snapshot):
        """Test creating a full user note"""

        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="user-note-test", description="testing user notes")

        # Create a user note
        query = """
        mutation makeUserNote {
          createUserNote(input: {
            owner: "default",
            labbookName: "user-note-test",
            title: "I think this is a thing",
            body: "##AND THIS IS A BODY\\n- asdggf\\n-asdf",
            tags: ["this", "and", "that"]
          })
          {
            newActivityRecordEdge {
                node{
                  message
                  detailObjects{                
                    data
                    type
                    show
                    importance
                    tags
                  }
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

    def test_create_user_note_check_vals(self, fixture_working_dir, snapshot):
        """Test to make sure keys and IDs are getting set OK"""
        # Create labbook
        lb = LabBook(fixture_working_dir[0])
        lb.new(owner={"username": "default"}, name="user-note-test", description="testing user notes")

        # Create a user note
        query = """
        mutation makeUserNote {
          createUserNote(input: {
            owner: "default",
            labbookName: "user-note-test",
            title: "I think this is a thing",
            body: "##AND THIS IS A BODY\\n- asdggf\\n-asdf",
            tags: ["this", "and", "that"]
          })
          {
            newActivityRecordEdge {
                node{
                  message
                  detailObjects{    
                    id
                    key            
                    data
                    type
                    show
                    importance
                    tags
                  }
                  id
                  commit
                  linkedCommit
                  type
                  show
                  importance
                  tags
              }
              cursor
            }
          }
        }
        """
        result = fixture_working_dir[2].execute(query)

        assert len(result['data']['createUserNote']['newActivityRecordEdge']['node']['id']) > 10
        assert type(result['data']['createUserNote']['newActivityRecordEdge']['node']['id']) == str
        assert len(result['data']['createUserNote']['newActivityRecordEdge']['node']['commit']) == 40
        assert type(result['data']['createUserNote']['newActivityRecordEdge']['node']['commit']) == str
        assert result['data']['createUserNote']['newActivityRecordEdge']['node']['linkedCommit'] == "no-linked-commit"
        assert result['data']['createUserNote']['newActivityRecordEdge']['node']['message'] == "I think this is a thing"

        assert len(result['data']['createUserNote']['newActivityRecordEdge']['node']['detailObjects'][0]['id']) > 10
        assert type(result['data']['createUserNote']['newActivityRecordEdge']['node']['detailObjects'][0]['id']) == str
        assert len(result['data']['createUserNote']['newActivityRecordEdge']['node']['detailObjects'][0]['key']) > 10
        assert type(result['data']['createUserNote']['newActivityRecordEdge']['node']['detailObjects'][0]['key']) == str
        assert "AND THIS IS A BODY" in result['data']['createUserNote']['newActivityRecordEdge']['node']['detailObjects'][0]['data'][0][1]





