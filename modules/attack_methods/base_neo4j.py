from abc import ABC, abstractmethod

from neo4j import GraphDatabase

neo4j_driver = GraphDatabase.driver('bolt://@127.0.0.1:7687', auth=('neo4j', 'Password1'))


class BaseAttackMethod(ABC):
    def __init__(self):
        pass

    def calc_query(self):
        def add_to_neo(tx):
            edges_types = self.get_edge_types()
            query = 'MATCH (input  {{node_type: "{0}"}}), (b) '.format(self.get_source_node())
            for i in range(len(edges_types)):
                query = query + 'MATCH p{0} = (user)-[:SystemConnection *]->(b) '.format(str(i))
            query = query + 'WHERE '
            all_rel_conds = []
            for i in range(len(edges_types)):
                all_rel_conds.append('ALL(r IN rels(p{0}) WHERE TYPE(r) = "SystemConnection")'.format(str(i)))
                all_rel_conds.append('last(rels(p{0})).type = "{1}"'.format(str(i), edges_types[i]))
                all_rel_conds.append('NONE(r IN tail(nodes(p{0})) WHERE r.node_type = "{1}")'.format(str(i), self.get_source_node()))

            query = query + ' AND '.join(all_rel_conds)
            all_node_conds = []
            if len(edges_types) > 1:
                for i in range(len(edges_types)):
                    all_node_conds.append('last(nodes(p{0})).NodeId = last(nodes(p{1})).NodeId'.format(str(i), str(i+1)))
                    all_node_conds.append('head(nodes(p{0})).NodeId = head(nodes(p{1})).NodeId'.format(str(i), str(i+1)))
                    if i+1 >= len(edges_types)-1:
                        break
                query = query + ' AND ' + ' AND '.join(all_node_conds)
            query = query + ' MATCH (input2  { NodeId: head(nodes(p0)).NodeId }), (output { NodeId: last(nodes(p0)).NodeId })'
            query = query + ' MERGE (input2)-[:{0} {{Name: "{1}", weight: {2}}}]->(output) ;'.format(self.get_attack_class(), self.get_attack_name(), str(self.get_attack_difficult()))
            tx.run(query)
        with neo4j_driver.session() as session:
            session.write_transaction(add_to_neo)

    @abstractmethod
    def get_attack_name(self):
        pass

    def get_attack_class(self):
        return 'Attack'

    @abstractmethod
    def get_edge_types(self):
        pass

    @abstractmethod
    def get_target_node(self):
        pass

    @abstractmethod
    def get_attack_difficult(self):
        pass

    @abstractmethod
    def get_source_node(self):
        pass
        # return ['StopInstance', 'DeaatchVolume', 'CreateInstance']