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
import graphene
from graphene.types import datetime

from lmcommon.labbook import LabBook
from lmcommon.logging import LMLogger
from lmcommon.activity import ActivityStore, ActivityDetailRecord, ActivityDetailType, ActivityType

from lmsrvcore.api.interfaces import GitRepository
from lmsrvcore.auth.user import get_logged_in_username
from lmsrvcore.api import logged_query

from lmsrvlabbook.dataloader.labbook import LabBookLoader

logger = LMLogger.get_logger()

# Bring ActivityType enumeration into Graphene
ActivityRecordTypeEnum = graphene.Enum.from_enum(ActivityType)

# Bring ActivityDeatilType enumeration into Graphene
ActivityDetailTypeEnum = graphene.Enum.from_enum(ActivityDetailType)


class ActivityDetailObject(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """Container for Activity Detail Records"""
    # An instance of the LabBook dataloader
    _dataloader = None
    _detail_record = None

    # Unique key for this activity detail record in the detail db
    key = graphene.String(required=True)

    # A list of data elements, encoded for the web, with the format [[MIME_TYPE, DATA],]
    data = graphene.List(graphene.List(graphene.String))

    # Type indicating the type of activity detail object
    type = graphene.Field(ActivityDetailTypeEnum)

    # Boolean indicating if this item should be "shown" or "hidden"
    show = graphene.Boolean()

    # A score indicating the importance, currently expected to range from 0-255
    importance = graphene.Int()

    # A list of tags for the entire record
    tags = graphene.List(graphene.String)

    def _load_detail_record(self):
        """Private method to load a detail record if it has not been previously loaded and set"""
        if not self._detail_record:
            # Load record from database
            if not self.key:
                raise ValueError("Must set `key` on object creation to resolve detail record")

            # Load store instance
            lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
            store = ActivityStore(lb)

            # Retrieve record
            self._detail_record: ActivityDetailRecord = store.get_detail_record(self.key)

        # Set class properties
        self.type = ActivityDetailTypeEnum.get(self._detail_record.type.value).value
        self.show = self._detail_record.show
        self.tags = self._detail_record.tags
        self.importance = self._detail_record.importance

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name, key = id.split("&")

        return ActivityDetailObject(id=f"{owner}&{name}&{key}", name=name, owner=owner, key=key,
                                    _dataloader=LabBookLoader())

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name or not self.key:
                raise ValueError("Resolving a ActivityDetailObject Node ID requires owner, name, and key to be set")
            self.id = f"{self.owner}&{self.name}&{self.key}"

        return self.id

    def resolve_type(self, info):
        """Resolve the type field"""
        if self.type is None:
            self._load_detail_record()
        return self.type

    def resolve_show(self, info):
        """Resolve the show field"""
        if self.show is None:
            self._load_detail_record()
        return self.show

    def resolve_importance(self, info):
        """Resolve the importance field"""
        if self.importance is None:
            self._load_detail_record()
        return self.importance

    def resolve_tags(self, info):
        """Resolve the tags field"""
        if self.tags is None:
            self._load_detail_record()
        return self.tags

    def resolve_data(self, info):
        """Resolve the data field"""
        if self.data is None:
            self._load_detail_record()

        # JSONify for transport via web
        data_dict = self._detail_record.jsonify_data()

        return [(x, data_dict[x]) for x in data_dict]


class ActivityRecordObject(graphene.ObjectType, interfaces=(graphene.relay.Node, GitRepository)):
    """Container for Activity Records"""
    # An instance of the LabBook dataloader
    _dataloader = None
    _activity_record = None

    # Commit hash for this activity record
    commit = graphene.String(required=True)

    # Commit hash of the commit this references
    linked_commit = graphene.String()

    # Message summarizing the Activity
    message = graphene.String()

    # Storage for detail objects
    detail_objects = graphene.List(ActivityDetailObject)

    # Type indicating the type of activity
    type = graphene.Field(ActivityRecordTypeEnum)

    # Boolean indicating if this item should be "shown" or "hidden"
    show = graphene.Boolean()

    # A score indicating the importance, currently expected to range from 0-255
    importance = graphene.Int()

    # A list of tags for the entire record
    tags = graphene.List(graphene.String)

    # Datetime of the record creation
    timestamp = datetime.DateTime()

    def _load_activity_record(self):
        """Private method to load an activity record if it has not been previously loaded and set"""
        if not self._activity_record:
            # Load record from database
            if not self.commit:
                raise ValueError("Must set `commit` on object creation to resolve detail record")

            # Load store instance
            lb = self._dataloader.load(f"{get_logged_in_username()}&{self.owner}&{self.name}").get()
            store = ActivityStore(lb)

            # Retrieve record
            self._activity_record = store.get_activity_record(self.commit)

        # Set class properties
        self.linked_commit = self._activity_record.linked_commit
        self.message = self._activity_record.message
        self.type = ActivityRecordTypeEnum.get(self._activity_record.type.value).value
        self.show = self._activity_record.show
        self.tags = self._activity_record.tags
        self.timestamp = self._activity_record.timestamp
        self.importance = self._activity_record.importance

    @classmethod
    def get_node(cls, info, id):
        """Method to resolve the object based on it's Node ID"""
        # Parse the key
        owner, name, commit = id.split("&")

        return ActivityDetailObject(id=f"{owner}&{name}&{commit}", name=name, owner=owner, commit=commit,
                                    _dataloader=LabBookLoader())

    def resolve_id(self, info):
        """Resolve the unique Node id for this object"""
        if not self.id:
            if not self.owner or not self.name or not self.commit:
                raise ValueError("Resolving a ActivityRecordObject Node ID requires owner, name, and commit to be set")
            self.id = f"{self.owner}&{self.name}&{self.commit}"

        return self.id

    def resolve_linked_commit(self, info):
        """Resolve the linked_commit field"""
        if self.linked_commit is None:
            self._load_activity_record()
        return self.linked_commit

    def resolve_message(self, info):
        """Resolve the message field"""
        if self.message is None:
            self._load_activity_record()
        return self.message

    def resolve_type(self, info):
        """Resolve the type field"""
        if self.type is None:
            self._load_activity_record()
        return self.type

    def resolve_show(self, info):
        """Resolve the show field"""
        if self.show is None:
            self._load_activity_record()
        return self.show

    def resolve_tags(self, info):
        """Resolve the tags field"""
        if self.tags is None:
            self._load_activity_record()
        return self.tags

    def resolve_timestamp(self, info):
        """Resolve the timestamp field"""
        if self.timestamp is None:
            self._load_activity_record()
        return self.timestamp

    def resolve_importance(self, info):
        """Resolve the importance field"""
        if self.importance is None:
            self._load_activity_record()
        return self.importance

    def resolve_detail_objects(self, info):
        """Resolve the detail_objects field"""
        if self.detail_objects is None:
            if self._activity_record is None:
                # Load the activity record first if it is missing
                self._load_activity_record()

            # Load detail objects from database
            self.detail_objects = [ActivityDetailObject(id=f"{self.owner}&{self.name}&{r[3].key}",
                                                        owner=self.owner,
                                                        name=self.name,
                                                        key=r[3].key,
                                                        _dataloader=self._dataloader) for r in self._activity_record.detail_objects]

        return self.detail_objects
