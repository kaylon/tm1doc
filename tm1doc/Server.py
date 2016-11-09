import requests
import json
import Process
import Dimension
import Cube
import Rule
import ODBC
import Text
import TM1Object
import networkx as nx

from config import *

class Server(object):
    """docstring for """



    def __init__(self, server_adress, server_user, server_password):
        self.server_adress = server_adress
        self.server_user = server_user
        self.server_password = server_password
        self.rules = []
        self.processes = []
        self.dimensions = []
        self.cubes = []
        self.texts = []
        self.odbcs = []
        self.__fetch_all()
        # self.subsets = []
        # self.views = []

    def __fetch_all(self):
        """ creates all server objects """
        # order is important here!
        self.__fetch_dimensions()
        self.__fetch_cubes()
        self.__fetch_rules()
        self.__fetch_processes()

    def create_dataflow_graph(self):
        dataflow_graph = nx.DiGraph()
        # add all cubes as nodes
        # add all dimension as nodes
        # add all dimension -- is part of --> cube edges
        for cube in self.cubes:
            dataflow_graph.add_node(cube)
            for dimension in cube.dimensions:
                """ TODO: fix!!! for more permanent stuff """
                edge_obj = TM1Object.TM1Object('is part of')
                # print(dimension)
                dataflow_graph.add_node(dimension)
                dataflow_graph.add_edge(dimension, cube, edge_object=edge_obj)
        # add all processes as edges and append other nodes if needed
        for process in self.processes:
            #map ALL THE SOURCES to all targets
            for source in process.data_sources:
                for target in process.data_targets:
                    dataflow_graph.add_node(source)
                    dataflow_graph.add_node(target)
                    dataflow_graph.add_edge(source, target, edge_object=process)
        # add all rules as edges and append other nodes if needed
        for rule in self.rules:
            for source in rule.data_sources:
                for target in rule.data_targets:
                    dataflow_graph.add_node(source)
                    dataflow_graph.add_node(target)
                    dataflow_graph.add_edge(source, target, edge_object=rule)
        return dataflow_graph

    def get_dataflow_for_graphviz(self, data_flow, graph_label, show_edge_labels=False):
        # remove technical elements

        graphviz_input = ''
        if IGNORE_TECHNICAL_OBJECTS:
            for node in data_flow.nodes():
                if node.name[:1] == '}':
                    data_flow.remove_node(node)
        # ignore dimensions for now
        for node in data_flow.nodes():
            if node.get_class_name() == 'Dimension':
                data_flow.remove_node(node)
        # remove nodes without flow
        for node in data_flow.nodes():
            if data_flow.out_degree(node) == 0 and data_flow.in_degree(node) == 0:
                data_flow.remove_node(node)


        graphviz_input += 'digraph '+graph_label+' {'
        graphviz_input += 'rankdir = LR;'
        # nodes
        for node in data_flow.nodes(): #_iter(data = True):
            tm1_object = node
            if IGNORE_TECHNICAL_OBJECTS and tm1_object.name[:1] == '}':
                continue
            try:
                node_class = tm1_object.get_class_name()
                # if node_class == 'Dimension':
                #     continue
            except:
                node_class = False
            if node_class == 'Dimension':
                #continue
                shape = 'box'
                fillcolor = 'red'
            elif node_class == 'Cube':
                shape = 'box3d'
                fillcolor = 'deeppink'
            elif node_class in  ['Flatfile', 'Text']:
                shape = 'folder'
                fillcolor = 'gold'
            elif node_class == 'ODBC':
                shape = 'box'
                fillcolor = 'deepskyblue'
            else:
                shape = 'ellipse'
                fillcolor = 'orange'
            graphviz_input += '"' + node.name + '" [ shape=' + shape + ' fillcolor='+fillcolor+ ' style = filled]'
        # edges
        for edge in data_flow.edges_iter(data=True):
            edge_object = edge[2]['edge_object']
            if IGNORE_TECHNICAL_OBJECTS and edge_object.name[:1] == '}':
                continue
            edge_color = 'black'
            if edge_object.get_class_name() == 'Rule':
                edge_color = 'navy'
            if edge_object.get_class_name() == 'Process':
                edge_color = 'seagreen'

            # edge_styl

            if show_edge_labels:
                label = '[ label = "'+ edge_object.name +'" color = ' + edge_color+ ']'
                graphviz_input += '"' + edge[0].name + '" -> "' + edge[1].name + '" '+label+';'
                # raise NotImplementedError
            else:
                label = '[ color = ""' + edge_color + '" "]'
                graphviz_input += '"' + edge[0].name + '" -> "' + edge[1].name + '" ' + label + ';'
        graphviz_input += '}'

        return graphviz_input

    def get_unused_dimensions():
        raise NotImplementedError( 'not supported' )

    def call_api(self, call_method):
        """ calls REST API with method

        ToDo: implement Certificate and reenable CERT checking

        """
        rest_call = self.server_adress + call_method

        call_result = requests.get(rest_call, auth=(self.server_user, self.server_password), verify=SERVER_CERTIFICATE_VERIFY)
        if(call_result.ok):
            # just deal with the json format - content is expected to be in 'value'
            result = json.loads(call_result.text)
            result = result['value']
        else:
            print('Could not estabish connection to REST API')
            call_result.raise_for_status()
        return result

    def get_object_by_name_from_list(self, name, list):
        """ returns object handle or None by name from any list of objects that have object.name attribute
        It is case insensitive!

        ToDo: exception handling if *Class*.name not applicable
        """
        ret = None
        for canidate in list:
            if canidate.name.lower() == name.lower():
                ret = canidate
        return ret

    def get_tm1object_by_type_and_name(self, object_type, object_name, create_object = False):
        tm1_object = None
        if object_type == 'None':
            tm1_object = None
        elif object_type == 'ODBC':
            tm1_object = self.get_object_by_name_from_list(object_name, self.odbcs)
            if tm1_object is None and create_object:
                tm1_object = ODBC.ODBC(object_name)
                self.odbcs.append(tm1_object)
        elif object_type == 'Process':
            tm1_object = self.get_object_by_name_from_list(object_name, self.processes)
        elif object_type == 'Rule':
            tm1_object = self.get_object_by_name_from_list(object_name, self.rules)
        elif object_type == 'Cube':
            tm1_object = self.get_object_by_name_from_list(object_name, self.cubes)
        elif object_type == 'Dimension':
            tm1_object = self.get_object_by_name_from_list(object_name, self.dimensions)
        elif object_type == 'Text':
            tm1_object = self.get_object_by_name_from_list(object_name, self.texts)
            if tm1_object is None and create_object:
                tm1_object = Text.Text(object_name)
                self.texts.append(tm1_object)
        return tm1_object

    def __fetch_processes(self):
        call_method = 'Processes'
        processes = self.call_api(call_method)
        self.processes = []
        for process_json in processes:
            process = Process.Process(process_json, self)
            self.processes.append(process)

    def __fetch_dimensions(self):
        call_method = 'Dimensions'
        dimensions = self.call_api(call_method)
        self.dimensions = []
        for dimension_json in dimensions:
            dimension = Dimension.Dimension(dimension_json, self)
            self.dimensions.append(dimension)

    def __fetch_cubes(self):
        call_method = 'Cubes?$expand=Dimensions'
        cubes = self.call_api(call_method)
        self.cubes = []
        for cube_json in cubes:
            cube = Cube.Cube(cube_json, self)
            self.cubes.append(cube)

    def __fetch_rules(self):
        call_method = 'Cubes'
        rules = self.call_api(call_method)
        self.rules = []
        for rule_json in rules:
            if rule_json['Rules'] != None:
                rule = Rule.Rule(rule_json, self)
                self.rules.append(rule)

    def get_Configuration(self):
        # get via api
        # or get from cfg file
        raise NotImplementedError( 'not supported' )

    def get_rules():
        raise NotImplementedError( 'not supported' )


    def get_cubes():
        raise NotImplementedError( 'not supported' )

    def get_dimensions():
        raise NotImplementedError( 'not supported' )
