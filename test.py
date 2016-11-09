import requests
import json

from config import *
from tm1doc import Server


# testing log calls!



tm1_server = Server.Server(SERVER_API_PATH, SERVER_USER, SERVER_PASSWORD)


call = 'Processes'
res = tm1_server.call_api(call)

# # log files of a day
# call = 'MessageLogEntries?$filter=TimeStamp ge datetimeoffset\'2016-09-10T01:01:00.000Z\' and TimeStamp lt datetimeoffset\'2016-10-01T01:01:59.999Z\'&$orderby=TimeStamp'
#
# res = tm1_server.call_api(call)
# #
# # # do prettyprint
# # parsed = json.loads(res)
# # print json.dumps(res, indent=4, sort_keys=True)
# # #
# def pp_json(json_thing, sort=True, indents=4):
#     if type(json_thing) is str:
#         print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
#     else:
#         print(json.dumps(json_thing, sort_keys=sort, indent=indents))
#     return None
#
# pp_json(res)

# # print(res)
#

# graph = tm1_server.create_dataflow_graph()
# tm1_server.render_dataflow_graph(graph, 'TestGraph', show_edge_labels=SHOW_EDGE_LABELS)
