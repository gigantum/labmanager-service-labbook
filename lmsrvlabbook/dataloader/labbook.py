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
from typing import List

from promise import Promise
from promise.dataloader import DataLoader

from lmcommon.labbook import LabBook
from lmsrvcore.auth.user import get_logged_in_author


class LabBookLoader(DataLoader):
    """Dataloader for lmcommon.labbook.LabBook instances

    The key for this object is username&owner&labbook_name
    """

    @staticmethod
    def get_labbook_instance(key: str):
        # Get identifying info from key
        username, owner_name, labbook_name = key.split('&')

        # Create Labbook instance
        lb = LabBook(author=get_logged_in_author())
        lb.from_name(username, owner_name, labbook_name)

        return lb

    def batch_load_fn(self, keys: List[str]):
        """Method to load labbook objects based on a list of unique keys

        Args:
            keys(list(str)): Unique key to identify the labbook

        Returns:

        """
        return Promise.resolve([self.get_labbook_instance(key) for key in keys])
