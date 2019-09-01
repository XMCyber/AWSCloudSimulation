from abc import ABC, abstractmethod
from modules import should_refresh


class JoinTopics:
    def __init__(self, storage, topics, keys_callback, relation_name, get_nodes):
        self.storage = storage
        self.topics = topics
        self.keys_callback = keys_callback
        self.get_nodes = get_nodes
        self.relation_name = relation_name
        if len(topics) > 2:
            raise Exception("Only under two topics are supported")

    def run(self):
        all_topics = {}
        for topic in self.topics:
            all_topics[topic] = self.storage.all_records(topic)

        if len(self.topics) == 1:
            for record in all_topics[self.topics[0]]:
                key_cb = self.keys_callback[0](record)
                if key_cb == -1:
                    continue
                nodes = self.get_nodes([record])
                nodes[0].relate(self.storage, nodes[1], self.relation_name)
        elif len(self.topics) == 2:
            for record in all_topics[self.topics[0]]:
                key_cb = self.keys_callback[0](record)
                if key_cb == -1:
                    continue
                for record2 in all_topics[self.topics[1]]:
                    key_cb2 = self.keys_callback[1](record2)
                    if key_cb2 == -1:
                        continue
                    if key_cb2 != key_cb:
                        continue
                    nodes = self.get_nodes([record, record2])
                    nodes[0].relate(self.storage, nodes[1], self.relation_name)


class NodesAndRelationshipsBase(ABC):
    def __init__(self, storage):
        self.storage = storage

    @staticmethod
    def should_cache():
        return False

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def get_relation_name(self):
        pass

    def run(self):
        topic_name = 'relations_' + self.get_relation_name()
        if not self.should_cache() or should_refresh.should_refresh(topic_name):
            self.init()
        should_refresh.update(topic_name)

