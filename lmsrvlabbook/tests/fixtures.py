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
import tempfile
import os
import uuid
import shutil
import graphene
from flask import Flask
import flask
import json
import time
from mock import patch
import responses
from graphene.test import Client

from lmcommon.environment import RepositoryManager
from lmcommon.configuration import Configuration, get_docker_client
from lmcommon.auth.identity import get_identity_manager
from lmcommon.labbook import LabBook
from lmsrvcore.middleware import LabBookLoaderMiddleware, error_middleware
from lmsrvcore.tests.fixtures import insert_cached_identity

from lmcommon.fixtures import (ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_REV, ENV_UNIT_TEST_BASE)
from lmcommon.container.container import ContainerOperations
from lmcommon.environment import ComponentManager
from lmcommon.imagebuilder import ImageBuilder

from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations


def _create_temp_work_dir(lfs_enabled: bool = True):
    """Helper method to create a temporary working directory and associated config file"""
    # Create a temporary working directory
    temp_dir = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
    os.makedirs(temp_dir)

    config = Configuration()
    # Make sure the "test" environment components are always used
    config.config["environment"]["repo_url"] = ["https://github.com/gig-dev/components2.git"]
    config.config["flask"]["DEBUG"] = False
    # Set the working dir to the new temp dir
    config.config["git"]["working_directory"] = temp_dir
    config.config["git"]["lfs_enabled"] = lfs_enabled
    # Set the auth0 client to the test client (only contains 1 test user and is partitioned from prod)
    config.config["auth"]["audience"] = "io.gigantum.api.dev"
    config.config["auth"]["client_id"] = "Z6Wl854wqCjNY0D4uJx8SyPyySyfKmAy"
    config_file = os.path.join(temp_dir, "temp_config.yaml")
    config.save(config_file)
    os.environ['HOST_WORK_DIR'] = temp_dir

    return config_file, temp_dir


class EnvironMock(object):
    """A simple class to mock the Flask environ object so you can have a token"""
    def __init__(self):
        self.environ = {'HTTP_AUTHORIZATION': "Bearer afaketoken"}


class ContextMock(object):
    """A simple class to mock the Flask request context so you have a labbook_loader attribute"""
    def __init__(self):
        self.labbook_loader = None
        self.headers = EnvironMock()


@pytest.fixture
def fixture_working_dir():
    """A pytest fixture that creates a temporary working directory, config file, schema, and local user identity
    """
    # Create temp dir
    config_file, temp_dir = _create_temp_work_dir()

    # Create user identity
    insert_cached_identity(temp_dir)

    # Create test client
    schema = graphene.Schema(query=LabbookQuery, mutation=LabbookMutations)

    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        # Load User identity into app context
        app = Flask("lmsrvlabbook")
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

        with app.app_context():
            # within this block, current_app points to app. Set current usert explicitly(this is done in the middleware)
            flask.g.user_obj = app.config["LABMGR_ID_MGR"].get_user_profile()

            # Create a test client
            client = Client(schema, middleware=[LabBookLoaderMiddleware()], context_value=ContextMock())

            yield config_file, temp_dir, client, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def fixture_working_dir_lfs_disabled():
    """A pytest fixture that creates a temporary working directory, config file, schema, and local user identity
    """
    # Create temp dir
    config_file, temp_dir = _create_temp_work_dir(lfs_enabled=False)

    # Create user identity
    insert_cached_identity(temp_dir)

    # Create test client
    schema = graphene.Schema(query=LabbookQuery, mutation=LabbookMutations)

    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        # Load User identity into app context
        app = Flask("lmsrvlabbook")
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

        with app.app_context():
            # within this block, current_app points to app. Set current usert explicitly(this is done in the middleware)
            flask.g.user_obj = app.config["LABMGR_ID_MGR"].get_user_profile()

            # Create a test client
            client = Client(schema, middleware=[LabBookLoaderMiddleware()], context_value=ContextMock())

            yield config_file, temp_dir, client, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="class")
def fixture_working_dir_env_repo_scoped():
    """A pytest fixture that creates a temporary working directory, a config file to match, creates the schema,
    and populates the environment component repository.
    Class scope modifier attached
    """
    # Create temp dir
    config_file, temp_dir = _create_temp_work_dir()

    # Create user identity
    insert_cached_identity(temp_dir)

    # Create test client
    schema = graphene.Schema(query=LabbookQuery, mutation=LabbookMutations)

    # get environment data and index
    erm = RepositoryManager(config_file)
    erm.update_repositories()
    erm.index_repositories()

    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        # Load User identity into app context
        app = Flask("lmsrvlabbook")
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

        with app.app_context():
            # within this block, current_app points to app. Set current user explicitly (this is done in the middleware)
            flask.g.user_obj = app.config["LABMGR_ID_MGR"].get_user_profile()

            # Create a test client
            client = Client(schema, middleware=[LabBookLoaderMiddleware(), error_middleware], context_value=ContextMock())

            yield config_file, temp_dir, client, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="class")
def fixture_working_dir_populated_scoped():
    """A pytest fixture that creates a temporary working directory, a config file to match, creates the schema,
    and populates the environment component repository.
    Class scope modifier attached
    """
    # Create temp dir
    config_file, temp_dir = _create_temp_work_dir()

    # Create user identity
    insert_cached_identity(temp_dir)

    # Create test client
    schema = graphene.Schema(query=LabbookQuery, mutation=LabbookMutations)

    # Create a bunch of lab books
    lb = LabBook(config_file)

    lb.new(owner={"username": "default"}, name="labbook1", description="Cats labbook 1")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook2", description="Dogs labbook 2")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook3", description="Mice labbook 3")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook4", description="Horses labbook 4")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook5", description="Cheese labbook 5")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook6", description="Goat labbook 6")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook7", description="Turtle labbook 7")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook8", description="Lamb labbook 8")
    time.sleep(1.1)
    lb.new(owner={"username": "default"}, name="labbook9", description="Taco labbook 9")
    time.sleep(1.1)
    lb.new(owner={"username": "test3"}, name="labbook-0", description="This should not show up.")

    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        # Load User identity into app context
        app = Flask("lmsrvlabbook")
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

        with app.app_context():
            # within this block, current_app points to app. Set current user explicitly (this is done in the middleware)
            flask.g.user_obj = app.config["LABMGR_ID_MGR"].get_user_profile()

            # Create a test client
            client = Client(schema, middleware=[LabBookLoaderMiddleware()], context_value=ContextMock())

            yield config_file, temp_dir, client, schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope='class')
def build_image_for_jupyterlab():
    # Create temp dir
    config_file, temp_dir = _create_temp_work_dir()

    # Create user identity
    insert_cached_identity(temp_dir)

    # Create test client
    schema = graphene.Schema(query=LabbookQuery, mutation=LabbookMutations)

    # get environment data and index
    erm = RepositoryManager(config_file)
    erm.update_repositories()
    erm.index_repositories()

    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        # Load User identity into app context
        app = Flask("lmsrvlabbook")
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

        with app.app_context():
            # within this block, current_app points to app. Set current user explicitly (this is done in the middleware)
            flask.g.user_obj = app.config["LABMGR_ID_MGR"].get_user_profile()

            # Create a test client
            client = Client(schema, middleware=[LabBookLoaderMiddleware(), error_middleware], context_value=ContextMock())

            # Create a labook
            lb = LabBook(config_file)
            lb.new(name="containerunittestbook", description="Testing docker building.",
                   owner={"username": "unittester"}, username="default")

            # Create Component Manager
            cm = ComponentManager(lb)
            # Add a component
            cm.add_component("base", ENV_UNIT_TEST_REPO, ENV_UNIT_TEST_BASE, ENV_UNIT_TEST_REV)
            cm.add_packages("pip3", [{"manager": "pip3", "package": "requests", "version": "2.18.4"}])

            ib = ImageBuilder(lb)
            ib.assemble_dockerfile(write=True)
            docker_client = get_docker_client()

            try:
                lb, docker_image_id = ContainerOperations.build_image(labbook=lb, username="default")

                yield lb, ib, docker_client, docker_image_id, client, "unittester"

            finally:
                try:
                    docker_client.containers.get(docker_image_id).stop()
                    docker_client.containers.get(docker_image_id).remove()
                except:
                    pass

                try:
                    docker_client.images.remove(docker_image_id, force=True, noprune=False)
                except:
                    pass

                shutil.rmtree(lb.root_dir)


@pytest.fixture
def fixture_test_file():
    """A pytest fixture that creates a temporary file
    """
    temp_file_name = os.path.join(tempfile.tempdir, "test_file.txt")
    with open(temp_file_name, 'wt') as dummy_file:
        dummy_file.write("blah")
        dummy_file.flush()
        dummy_file.seek(0)

        yield dummy_file.name

    try:
        os.remove(temp_file_name)
    except:
        pass

@pytest.fixture()
def property_mocks_fixture():
    """A pytest fixture that returns a GitLabRepositoryManager instance"""
    responses.add(responses.GET, 'https://usersrv.gigantum.io/key',
                  json={'key': 'afaketoken'}, status=200)
    responses.add(responses.GET, 'https://repo.gigantum.io/api/v4/projects?search=labbook1',
                  json=[{
                          "id": 26,
                          "description": "",
                        }],
                  status=200, match_querystring=True)
    yield


@pytest.fixture()
def docker_socket_fixture():
    """Helper method to get the docker client version"""
    client = get_docker_client()
    version = client.version()['ApiVersion']

    if "CIRCLECI" in os.environ:
        docker_host = os.environ['DOCKER_HOST']
        docker_host = docker_host.replace("tcp", "https")
        responses.add_passthru(
            f"{docker_host}/v{version}/images/default-default-labbook1/json")
        responses.add_passthru(
            f"{docker_host}/v{version}/containers/default-default-labbook1/json")
        responses.add_passthru(
            f"{docker_host}/v{version}/images/default-default-labbook1/json")
        responses.add_passthru(
            f"{docker_host}/v{version}/containers/default-default-labbook1/json")
        responses.add_passthru(
            f"{docker_host}/v{version}/images/default-test-sample-repo-lb/json")
        responses.add_passthru(
            f"{docker_host}/v{version}/containers/default-test-sample-repo-lb/json")
        responses.add_passthru(
            #'http+docker://35.196.196.144:2376/v1.30/containers/default-test-sample-repo-lb/json')
            '{docker_host}/v{version}/containers/default-test-sample-repo-lb/json')
    else:
        responses.add_passthru(
            f"http+docker://localunixsocket/v{version}/images/default-default-labbook1/json")
        responses.add_passthru(
            f"http+docker://localunixsocket/v{version}/containers/default-default-labbook1/json")
        responses.add_passthru(
            f"http+docker://localunixsocket/v{version}/images/default-test-sample-repo-lb/json")
        responses.add_passthru(
            f"http+docker://localunixsocket/v{version}/containers/default-test-sample-repo-lb/json")

    yield
