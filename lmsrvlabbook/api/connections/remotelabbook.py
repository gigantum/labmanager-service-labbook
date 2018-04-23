# Copyright (c) 2018 FlashX, LLC
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
import graphene
from lmsrvlabbook.api.objects.remotelabbook import RemoteLabbook


class RemoteLabbookConnection(graphene.relay.Connection):
    """A Connection for paging through remote labbooks.

    This is a remote call, so should be fetched on its own and only when needed. The user must have a valid
    session for data to be returned.

    It is recommended to use large page size (e.g. 50-100). This is due to how the remote server returns all the
    available data at once, so it is more efficient to load a lot of records at a time.

    Supported sorting modes:
        - az: naturally sort
        - created_on: sort by creation date, newest first
        - modified_on: sort by modification date, newest first
    """
    class Meta:
        node = RemoteLabbook


