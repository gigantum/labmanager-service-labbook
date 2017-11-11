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
import json
from mock import patch

from lmcommon.configuration import Configuration
from lmcommon.auth.identity import get_identity_manager

from lmsrvlabbook.api.query import LabbookQuery
from lmsrvlabbook.api.mutation import LabbookMutations


# Create ObjectType clases, since the EnvironmentQueries and EnvironmentMutations
# are abstract (allowing multiple inheritance)
class Query(LabbookQuery, graphene.ObjectType):
    pass


class Mutation(LabbookMutations, graphene.ObjectType):
    pass


def _create_temp_work_dir():
    """Helper method to create a temporary working directory and associated config file"""
    # Create a temporary working directory
    temp_dir = os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)
    os.makedirs(temp_dir)

    config = Configuration()
    config.config["git"]["working_directory"] = temp_dir
    config.config["auth"]["audience"] = "io.gigantum.api.dev"
    config_file = os.path.join(temp_dir, "temp_config.yaml")
    config.save(config_file)

    return config_file, temp_dir


@pytest.fixture
def fixture_working_dir():
    """A pytest fixture that creates a temporary working directory, config file, schema, and local user identity
    """
    # Create temp dir
    config_file, temp_dir = _create_temp_work_dir()

    # Create user identity
    user_dir = os.path.join(temp_dir, '.labmanager', 'identity')
    os.makedirs(user_dir)
    with open(os.path.join(user_dir, 'user.json'), 'wt') as user_file:
        json.dump({"username": "default",
                   "email": "jane@doe.com",
                   "given_name": "Jane",
                   "family_name": "Doe"}, user_file)

    # Create test client
    schema = graphene.Schema(query=Query, mutation=Mutation)

    with patch.object(Configuration, 'find_default_config', lambda self: config_file):
        app = Flask("lmsrvlabbook")

        # Load configuration class into the flask application
        app.config["LABMGR_CONFIG"] = Configuration()
        app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

        with app.app_context():
            # within this block, current_app points to app.
            yield config_file, temp_dir, schema  # name of the config file, temporary working directory, the schema

    # Remove the temp_dir
    shutil.rmtree(temp_dir)