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
import shutil
import os
import base64
import subprocess

from confhttpproxy import ProxyRouter
from flask import Flask, jsonify, request, abort
import flask
from flask_cors import CORS, cross_origin
import redis
import blueprint


from lmcommon.configuration import Configuration
from lmcommon.logging import LMLogger
from lmcommon.environment import RepositoryManager
from lmcommon.auth.identity import AuthenticationError, get_identity_manager
from lmcommon.labbook.lock import reset_all_locks
from lmcommon.labbook import LabBook
from lmsrvcore.auth.user import get_logged_in_author


logger = LMLogger.get_logger()

# Create Flask app
app = Flask("lmsrvlabbook")

# Load configuration class into the flask application
random_bytes = os.urandom(32)
app.config["SECRET_KEY"] = base64.b64encode(random_bytes).decode('utf-8')
app.config["LABMGR_CONFIG"] = config = Configuration()
app.config["LABMGR_ID_MGR"] = get_identity_manager(Configuration())

if config.config["flask"]["allow_cors"]:
    # Allow CORS
    CORS(app, max_age=7200)

# Set Debug mode
app.config['DEBUG'] = config.config["flask"]["DEBUG"]

# Register LabBook service
app.register_blueprint(blueprint.complete_labbook_service)

# Configure CHP
try:
    api_prefix = app.config["LABMGR_CONFIG"].config['proxy']["labmanager_api_prefix"]
    apparent_proxy_port = app.config["LABMGR_CONFIG"].config['proxy']["apparent_proxy_port"]
    api_port = app.config["LABMGR_CONFIG"].config['proxy']['api_port']

    proxy_router = ProxyRouter.get_proxy(app.config["LABMGR_CONFIG"].config['proxy'])
    proxy_router.add("http://localhost:10001", "api")
    logger.info(f"Proxy routes ({type(proxy_router)}): {proxy_router.routes}")
except Exception as e:
    logger.exception(e)


# Set auth error handler
@app.errorhandler(AuthenticationError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# Set Unauth'd route for API health-check
@app.route(f"{api_prefix}/ping/")
@cross_origin(headers=["Content-Type", "Authorization"], max_age=7200)
def ping():
    """Unauthorized endpoint for validating the API is up"""
    return jsonify(config.config['build_info'])


@app.route(f'{api_prefix}/savehook/<username>/<owner>/<labbook_name>')
def savehook(username, owner, labbook_name):
    try:
        changed_file = request.args.get('file')
        jupyter_token = request.args.get('jupyter_token')
        logger.debug(f"Received save hook for {changed_file} in {username}/{owner}/{labbook_name}")

        redis_conn = redis.Redis(db=1)
        lb_jupyter_token_key = '-'.join(['gmlb', username, owner, labbook_name, 'jupyter-token'])
        lb_active_key = f"{'|'.join([username, owner, labbook_name])}&is-busy*"

        r = redis_conn.get(lb_jupyter_token_key.encode())
        if r is None:
            logger.error(f"Could not find jupyter token for {username}/{owner}/{labbook_name}")
            abort(400)

        if r.decode() != jupyter_token:
            raise ValueError("Incoming jupyter token must be valid")

        if len(redis_conn.keys(lb_active_key.encode())) > 0:
            # A kernel in this project is still active. Don't save auto-commit because it can blow up the
            # repository size depending on what the user is doing
            logger.info(f"Skipping jupyter savehook for {username}/{owner}/{labbook_name} due to active kernel")
            return 'success'

        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner, labbook_name)
        with lb.lock_labbook():
            lb.sweep_uncommitted_changes()

        logger.info(f"Jupyter save hook saved {changed_file} from {str(lb)}")
        return 'success'
    except Exception as err:
        logger.error(err)
        return abort(400)


# TEMPORARY KLUDGE
# Due to GitPython implementation, resources leak. This block deletes all GitPython instances at the end of the request
# Future work will remove GitPython, at which point this block should be removed.
@app.after_request
def cleanup_git(response):
    loader = getattr(flask.request, 'labbook_loader', None)
    if loader:
        for key in loader.__dict__["_promise_cache"]:
            try:
                lb = loader.__dict__["_promise_cache"][key].value
                lb.git.repo.__del__()
            except AttributeError:
                continue
    return response
# TEMPORARY KLUDGE


logger.info("Cloning/Updating environment repositories.")

try:
    erm = RepositoryManager()
    update_successful = erm.update_repositories()
    if update_successful:
        logger.info("Indexing environment repositories.")
        erm.index_repositories()
        logger.info("Environment repositories updated and ready.")

    else:
        logger.info("Unable to update environment repositories at startup, most likely due to lack of internet access.")
except Exception as e:
    logger.error(e)
    raise

# Empty container-container share dir as it is ephemeral
share_dir = os.path.join(os.path.sep, 'mnt', 'share')
logger.info("Emptying container-container share folder: {}.".format(share_dir))
try:
    for item in os.listdir(share_dir):
        item_path = os.path.join(share_dir, item)
        if os.path.isfile(item_path):
            os.unlink(item_path)
        else:
            shutil.rmtree(item_path)
except Exception as e:
    logger.error(f"Failed to empty share folder: {e}.")
    raise

post_save_hook_code = """
import subprocess, os
def post_save_hook(os_path, model, contents_manager, **kwargs):
    try:
        labmanager_ip = open('/home/giguser/labmanager_ip').read().strip()
        tokens = open('/home/giguser/jupyter_token').read().strip()
        username, owner, lbname, jupyter_token = tokens.split(',')
        url_args = f'file={os.path.basename(os_path)}&jupyter_token={jupyter_token}'
        subprocess.run(['wget', '--spider', 
            f'http://{labmanager_ip}:10001/api/savehook/{username}/{owner}/{lbname}?{url_args}'], cwd='/tmp')
    except Exception as e:
        print(e)

"""
os.makedirs(os.path.join(share_dir, 'jupyterhooks'))
with open(os.path.join(share_dir, 'jupyterhooks', '__init__.py'), 'w') as initpy:
    initpy.write(post_save_hook_code)


# Reset distributed lock, if desired
if config.config["lock"]["reset_on_start"]:
    logger.info("Resetting ALL distributed locks")
    reset_all_locks(config.config['lock'])


def main(debug=False) -> None:
    try:
        # Run app on 0.0.0.0, assuming not an issue since it should be in a container
        # Please note: Debug mode must explicitly be set to False when running integration
        # tests, due to properties of Flask werkzeug dynamic package reloading.
        if debug:
            # This is to support integration tests, which will call main
            # with debug=False in order to avoid runtime reloading of Python code
            # which causes the interpreter to crash.
            app.run(host="0.0.0.0", port=10001, debug=debug)
        else:
            # If debug arg is not explicitly given then it is loaded from config
            app.run(host="0.0.0.0", port=10001)
    except Exception as e:
        logger.exception(e)
        raise


if __name__ == '__main__':
    main()
