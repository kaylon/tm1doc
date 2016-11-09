import requests
import json

from config import *
from tm1doc import Server


tm1_server = Server.Server(SERVER_API_PATH, SERVER_USER, SERVER_PASSWORD)

graph = tm1_server.create_dataflow_graph()
graphviz_input = tm1_server.get_dataflow_for_graphviz(graph, 'TM1_Dataflow', show_edge_labels=SHOW_EDGE_LABELS)
print(graphviz_input)



# for node in graph.nodes():
#     print node.name, node


# for node in graph.nodes():
#     print(node.name + ' out edges: ' + str(graph.out_degree(node)))
# for odbc in tm1_server.odbcs:
#     print odbc, odbc.name
# pro = tm1_server.get_tm1object_by_type_and_name('Process', 'dimension.companies.create')
#
# print(graph.out_degree(pro.data_sources[0]))
# print(pro.data_sources)
# print(pro.data_targets)
# for node in graph.successors(pro.data_sources[0]):
#     print node.name
#
# for node in graph.nodes():
#     print node.name

# for cube in tm1_server.processes:
#     print cube, cube.name





# check if objects were created
# for odbc in tm1_server.odbcs:
#     print(odbc.name)
#
# for text in tm1_server.texts:
#     print(text.name)



# debug
# for process in tm1_server.processes:
#     if process.name[:1] == '}':
#         continue
#     print process.name #+ ' : ' + process.data_source_type + ' -> ' + process.data_target
#     print process.data_sources
#     print '\n'
#     # print process.data_targets, process.get_data_target(), process.get_data_target_type()
#
# print '\n\n'

# for dimension in tm1_server.dimensions:
#     print dimension.name
#
# for cube in tm1_server.cubes:
#     cube.pretty_print()
#
# for rule in tm1_server.rules:
#     for source in rule.sources:
#         print('rule:' + source + ' -> ' + rule.name)
