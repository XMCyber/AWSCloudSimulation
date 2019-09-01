from abc import abstractmethod
from pyee import EventEmitter
from modules.info_gather.base_runner import BaseInfoGather
ee = EventEmitter()


class AWSBaseRunner(BaseInfoGather):
    pass