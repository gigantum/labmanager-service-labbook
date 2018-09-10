
import os
import io
import math
import pprint
import tempfile
import pytest
from graphene.test import Client
from werkzeug.datastructures import FileStorage

from lmcommon.labbook import LabBook
from lmcommon.files import FileOperations
from lmcommon.fixtures import remote_labbook_repo, mock_config_file
from lmsrvcore.middleware import LabBookLoaderMiddleware
from lmsrvlabbook.tests.fixtures import fixture_working_dir_env_repo_scoped, fixture_working_dir


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


class TestUploadFilesMutations(object):
    def test_add_file(self, mock_create_labbooks):
        """Test adding a new file to a labbook"""

        class DummyContext(object):
            def __init__(self, file_handle):
                self.labbook_loader = None
                self.files = {'uploadChunk': file_handle}

        client = Client(mock_create_labbooks[3], middleware=[LabBookLoaderMiddleware()])

        # Create file to upload
        test_file = os.path.join(tempfile.gettempdir(), "myValidFile.dat")
        est_size = 9000000
        try:
            os.remove(test_file)
        except:
            pass
        with open(test_file, 'wb') as tf:
            tf.write(os.urandom(est_size))

        new_file_size = os.path.getsize(tf.name)
        # Get upload params
        chunk_size = 4194000
        file_info = os.stat(test_file)
        file_size = int(file_info.st_size / 1000)
        total_chunks = int(math.ceil(file_info.st_size / chunk_size))

        target_file = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                   'labbook1', 'code', 'newdir', "myValidFile.dat")
        lb = LabBook(mock_create_labbooks[0])
        lb.from_directory(os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks', 'labbook1'))
        FileOperations.makedir(lb, 'code/newdir', create_activity_record=True)

        txid = "000-unitest-transaction"
        with open(test_file, 'rb') as tf:
            # Check for file to exist (shouldn't yet)
            assert os.path.exists(target_file) is False
            for chunk_index in range(total_chunks):
                # Upload a chunk
                chunk = io.BytesIO()
                chunk.write(tf.read(chunk_size))
                chunk.seek(0)
                file = FileStorage(chunk)

                query = f"""
                            mutation addLabbookFile{{
                              addLabbookFile(input:{{owner:"default",
                                                      labbookName: "labbook1",
                                                      section: "code",
                                                      filePath: "newdir/myValidFile.dat",
                                                      transactionId: "{txid}",
                                chunkUploadParams:{{
                                  uploadId: "fdsfdsfdsfdfs",
                                  chunkSize: {chunk_size},
                                  totalChunks: {total_chunks},
                                  chunkIndex: {chunk_index},
                                  fileSizeKb: {file_size},
                                  filename: "{os.path.basename(test_file)}"
                                }}
                              }}) {{
                                      newLabbookFileEdge {{
                                        node{{
                                          id
                                          key
                                          isDir
                                          size
                                        }}
                                      }}
                                    }}
                            }}
                            """
                r = client.execute(query, context_value=DummyContext(file))
        assert 'errors' not in r
        # So, these will only be populated once the last chunk is uploaded. Will be None otherwise.
        assert r['data']['addLabbookFile']['newLabbookFileEdge']['node']['isDir'] is False
        assert r['data']['addLabbookFile']['newLabbookFileEdge']['node']['key'] == 'newdir/myValidFile.dat'
        assert r['data']['addLabbookFile']['newLabbookFileEdge']['node']['size'] == f"{new_file_size}"
        # When done uploading, file should exist in the labbook
        assert os.path.exists(target_file)
        assert os.path.isfile(target_file)

        complete_query = f"""
        mutation completeQuery {{
            completeBatchUploadTransaction(input: {{
                owner: "default",
                labbookName: "labbook1",
                transactionId: "{txid}"
            }}) {{
                success
            }}
        }}
        """
        r = client.execute(complete_query, context_value=DummyContext(file))
        assert 'errors' not in r
        assert lb.is_repo_clean
        assert 'Uploaded 1 new file(s)' in lb.git.log()[0]['message']

    def test_add_file_fail_due_to_git_ignore(self, mock_create_labbooks):
        """Test adding a new file to a labbook"""

        class DummyContext(object):
            def __init__(self, file_handle):
                self.labbook_loader = None
                self.files = {'uploadChunk': file_handle}

        client = Client(mock_create_labbooks[3], middleware=[LabBookLoaderMiddleware()])

        new_file_size = 9000000
        # Create file to upload
        test_file = os.path.join(tempfile.gettempdir(), ".DS_Store")
        with open(test_file, 'wb') as tf:
            tf.write(os.urandom(new_file_size))

        # Get upload params
        chunk_size = 4194000
        file_info = os.stat(test_file)
        file_size = int(file_info.st_size / 1000)
        total_chunks = int(math.ceil(file_info.st_size / chunk_size))

        target_file = os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks',
                                   'labbook1', 'code', 'newdir', '.DS_Store')
        try:
            os.remove(target_file)
        except:
            pass
        lb = LabBook(mock_create_labbooks[0])
        lb.from_directory(os.path.join(mock_create_labbooks[1], 'default', 'default', 'labbooks', 'labbook1'))
        FileOperations.makedir(lb, 'code/newdir', create_activity_record=True)

        with open(test_file, 'rb') as tf:
            # Check for file to exist (shouldn't yet)
            assert os.path.exists(target_file) is False

            for chunk_index in range(total_chunks):
                # Upload a chunk
                chunk = io.BytesIO()
                chunk.write(tf.read(chunk_size))
                chunk.seek(0)
                file = FileStorage(chunk)

                query = f"""
                            mutation addLabbookFile{{
                              addLabbookFile(input:{{owner:"default",
                                                      labbookName: "labbook1",
                                                      section: "code",
                                                      filePath: "newdir/.DS_Store",
                                                      transactionId: "111-unittest-tx",
                                chunkUploadParams:{{
                                  uploadId: "jfdjfdjdisdjwdoijwlkfjd",
                                  chunkSize: {chunk_size},
                                  totalChunks: {total_chunks},
                                  chunkIndex: {chunk_index},
                                  fileSizeKb: {file_size},
                                  filename: "{os.path.basename(test_file)}"
                                }}
                              }}) {{
                                      newLabbookFileEdge {{
                                        node{{
                                          id
                                          key
                                          isDir
                                          size
                                        }}
                                      }}
                                    }}
                            }}
                            """
                r = client.execute(query, context_value=DummyContext(file))

            # This must be outside of the chunk upload loop
            pprint.pprint(r)
            assert 'errors' in r
            assert len(r['errors']) == 1
            assert 'matches ignored pattern' in r['errors'][0]['message']

        # When done uploading, file should exist in the labbook
        assert os.path.isfile(target_file) is False
        assert os.path.exists(target_file) is False

    def test_add_file_errors(self, mock_create_labbooks, snapshot):
        """Test new file error handling"""

        class DummyContext(object):
            def __init__(self, file_handle):
                self.labbook_loader = None
                self.files = {'blah': file_handle}

        client = Client(mock_create_labbooks[3])
        query = f"""
                    mutation addLabbookFile{{
                      addLabbookFile(input:{{owner:"default",
                                              labbookName: "labbook1",
                                              section: "code",
                                              filePath: "myfile.bin",
                                              transactionId: "999-unittest-transaction",
                        chunkUploadParams:{{
                          uploadId: "jfdjfdjdisdjwdoijwlkfjd",
                          chunkSize: 100,
                          totalChunks: 2,
                          chunkIndex: 0,
                          fileSizeKb: 200,
                          filename: "myfile.bin"
                        }}
                      }}) {{
                              newLabbookFileEdge {{
                                node{{
                                  id
                                  key
                                  isDir
                                  size
                                }}
                              }}
                            }}
                    }}
                    """
        # Fail because no file
        r = client.execute(query, context_value=DummyContext(None))
        assert 'errors' in r
        # DMK - commenting out test because check is currently disabled
        # test_file = os.path.join(tempfile.gettempdir(), "myfile.txt")

        # with open(test_file, 'wt') as tf:
        #     tf.write("THIS IS A FILE I MADE!")

        # with open(test_file, 'rb') as tf:
        #     file = FileStorage(tf)
        #     # Fail because filenames don't match
        #     snapshot.assert_match(client.execute(query, context_value=DummyContext(file)))
