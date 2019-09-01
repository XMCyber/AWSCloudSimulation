import datetime
from abc import ABC, abstractmethod


class BaseNode(ABC):
    @abstractmethod
    def get_labels(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    def get_data(self):
        return {'node_id': self.get_id_and_type(), 'node_resource_id': self.get_id(), 'node_type': self.get_labels()}

    @abstractmethod
    def get_node_type(self):
        pass

    def store(self, storage):
        return storage.upsert('graph_nodes', self.get_data(),
                                     (storage.where('node_id') == self.get_id_and_type()))

    def get_id_and_type(self):
        return self.get_node_type() + '_' + self.get_id()

    def relate(self, storage, node, relation_name, extra_data=None):
        if not extra_data:
            extra_data = {}

        our_id = self.get_id_and_type()
        remote_id = node.get_id_and_type()

        self.store(storage)
        node.store(storage)

        extra_data['relation_name'] = relation_name
        extra_data['source_node'] = our_id
        extra_data['target_node'] = remote_id

        condition = ((storage.where('source_node') == our_id)
                                 & (storage.where('relation_name') == relation_name)
                                 & (storage.where('target_node') == remote_id))

        storage.upsert('graph_relationships', extra_data, condition)

