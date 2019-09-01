import copy
import datetime
from abc import abstractmethod, ABC
from deepdiff import DeepDiff
from modules import should_refresh
import tinydb

GATHER_MAX_DATE = datetime.datetime(2050, 1, 1, 1, 1, 1, 1)


class BaseMessage(ABC):
    @abstractmethod
    def get_message_base_type(self):
        pass


class NewDataFound(BaseMessage):
    def __init__(self, data, start_time, end_time):
        self.data = data
        self.start_time = start_time
        self.end_time = end_time

    def get_message_base_type(self):
        return 'NewDataFound'


class DataRemoved(BaseMessage):
    def __init__(self, data, end_time):
        self.end_time = end_time
        self.data = data

    def get_message_base_type(self):
        return 'DataRemoved'


class DataUpdated(BaseMessage):
    def __init__(self, data, start_time, end_time, object_diff):
        self.data = data
        self.start_time = start_time
        self.end_time = end_time
        self.object_diff = object_diff

    def get_message_base_type(self):
        return 'DataUpdated'


DATA_CLASS_MAPPING = {'added': 'NewDataFound', 'updated': 'DataUpdated', 'removed': 'DataRemoved'}


class BaseInfoGather(ABC):
    def __init__(self, storage):
        self.storage = storage

    @abstractmethod
    def init(self):
        raise Exception("Unimplemented")

    @abstractmethod
    def get_topic_name(self):
        raise Exception("Unimplemented")

    def run(self):
        topic_name = 'gather_' + self.get_topic_name()
        if should_refresh.should_refresh(topic_name):
            self.init()
        should_refresh.update(topic_name)

    def save_data(self, data, condition, sub_topic=''):
        #copy_data = copy.deepcopy(data)
        copy_data = data
        self.storage.upsert(self.get_topic_name() + sub_topic, copy_data, condition)

