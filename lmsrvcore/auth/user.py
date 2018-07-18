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
import flask

from lmcommon.logging import LMLogger
from lmcommon.auth.user import User
from lmcommon.gitlib.git import GitAuthor
from lmsrvcore.auth.identity import get_identity_manager_instance


def get_logged_in_user() -> User:
    """A method to get the current logged in User object"""
    # Check for user in redis cache
    access_token = flask.g.get('access_token', None)
    id_token = flask.g.get('id_token', None)

    request_scoped_user = flask.g.get('user_obj', None)
    if not request_scoped_user:
        request_scoped_user = get_identity_manager_instance().get_user_profile(access_token, id_token)
        flask.g.user_obj = request_scoped_user

    return request_scoped_user


def get_logged_in_username():
    """A Method to get the current logged in user's username


    Returns:
        str
    """
    user = get_logged_in_user()

    if not user:
        logger = LMLogger()
        logger.logger.error("Failed to load a user identity from request context.")
        raise ValueError("Failed to load a user identity from request context.")

    return user.username


def get_logged_in_author():
    """A Method to get the current logged in user's GitAuthor instance


    Returns:
        GitAuthor
    """
    user = get_logged_in_user()

    if not user:
        logger = LMLogger()
        logger.logger.error("Failed to load a user identity from request context.")
        raise ValueError("Failed to load a user identity from request context.")

    # Create a GitAuthor instance if possible

    return GitAuthor(name=user.username, email=user.email)
