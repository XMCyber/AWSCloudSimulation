from modules import simple_storage
import csv


def export():
    all_nodes = simple_storage.all_records('graph_nodes')
    all_relations = simple_storage.all_records('graph_relationships')

    with open('graph_nodes.csv', 'w') as csvfile:
        fieldnames = ['node_id', 'node_resource_id', 'node_type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for graph_node in all_nodes:
            writer.writerow(graph_node)

    with open('graph_relationships.csv', 'w') as csvfile:
        fieldnames = ['relation_name', 'source_node', 'target_node']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for graph_relation in all_relations:
            writer.writerow(graph_relation)