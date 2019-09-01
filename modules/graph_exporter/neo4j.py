from neo4j import GraphDatabase
from modules import simple_storage
from modules import config

neo4j_driver = GraphDatabase.driver(config.config['NEO4J']['URL'], auth=(config.config['NEO4J']['USERNAME'], config.config['NEO4J']['PASSWORD']))


def add_to_neo(tx):
    all_nodes = simple_storage.all_records('graph_nodes')
    all_relations = simple_storage.all_records('graph_relationships')

    for node in all_nodes:
        tx.run('MERGE (t:{1} {{NodeId: "{0}", node_type: "{1}"}});'.format(node['node_id'], node['node_type']))

    for rel in all_relations:
        tx.run('MATCH (source {{NodeId: "{0}"}}), (target {{NodeId: "{1}"}}) MERGE (source)-[:SystemConnection {{type: "{2}"}}]->(target);'.format(rel['source_node'], rel['target_node'], rel['relation_name']))

def export():
    with neo4j_driver.session() as session:
        session.write_transaction(add_to_neo)


