from collections import OrderedDict
import requests
import json
import pandas as pd
from tm1doc.Process import Process
from tm1doc.Dimension import Dimension
from tm1doc.Cube import Cube
from tm1doc.Rule import Rule
from tm1doc.ODBC import ODBC
from tm1doc.Text import Text

from graphviz import Digraph

from TM1py.Services import TM1Service

from config import *


class Server(object):
    """docstring for """

    def __init__(self, server_adress, server_port, server_user, server_password, ssl_verify):
        self.server_adress = server_adress
        self.server_port = server_port
        self.server_user = server_user
        self.server_password = server_password
        self.ssl_verify = ssl_verify
        self.rules = []
        self.processes = []
        self.dimensions = []
        self.cubes = []
        self.texts = []
        self.odbcs = []
        self.__fetch_all()
        self.name = self.get_server_name()
        # self.subsets = []
        # self.views = []

    def __fetch_all(self):
        """ creates all server objects """
        # order is important here!
        self.__fetch_dimensions()
        self.__fetch_cubes()
        self.__fetch_rules()
        self.__fetch_processes()

    def get_source_to_dimension_mapping(self):

        dimensions = OrderedDict(
            (dimension.name, {'process': None, 'source': None, 'source_type': None}) for dimension in self.dimensions)

        for process in self.processes:
            # flow =  {'process_name'}
            # map ALL THE SOURCES to all targets
            for source in process.data_sources:
                for target in process.data_targets:
                    if target.__class__.__name__ == 'Dimension':
                        dimensions[target.name]['process'] = process.name
                        dimensions[target.name]['source'] = source.name
                        dimensions[target.name]['source_type'] = source.__class__.__name__

        # print(dimensions)
        return dimensions

    def create_dataflow_graph(self):
        dataflow_graph = Digraph(graph_attr={'rankdir': 'LR', 'ranksep': '0.25', 'nodesep': '0.1'}, strict=True)

        # add all cubes as nodes
        # add all dimension as nodes
        # add all dimension -- is part of --> cube edges
        cube_attributes = {'shape': 'box3d', 'style': 'solid', 'color': '#888888'}
        odbc_attributes = {'shape': 'cylinder', 'style': 'solid', 'color': 'blue'}
        process_attributes = {'color': 'green'}
        rule_attributes = {'color': 'navy'}

        for cube in self.cubes:

            if not cube.name.startswith('}'):
                dataflow_graph.node(name=cube.name, _attributes=cube_attributes)

                # for dimension in cube.dimensions:
                #    """ TODO: fix!!! for more permanent stuff """
                #    edge_obj = TM1Object.TM1Object('is part of')
                # print(dimension)
                # dataflow_graph.add_node(dimension)
                # dataflow_graph.add_edge(dimension, cube, edge_object=edge_obj)
                # dot.node(dimen)
        # add all processes as edges and append other nodes if needed

        for process in self.processes:
            # map ALL THE SOURCES to all targets
            for source in process.data_sources:
                for target in process.data_targets:
                    if target.__class__.__name__ == 'Cube':
                        dataflow_graph.node(name=source.name, label=source.name.replace('.', '\n'),
                                            _attributes=odbc_attributes)
                        dataflow_graph.node(name=target.name, _attributes=cube_attributes)
                        dataflow_graph.edge(source.name, target.name, label=process.name,
                                            _attributes=process_attributes)
        # add all rules as edges and append other nodes if needed

        for rule in self.rules:
            for source in rule.data_sources:
                for target in rule.data_targets:
                    dataflow_graph.node(name=source.name, _attributes=cube_attributes)
                    dataflow_graph.node(name=target.name, _attributes=cube_attributes)
                    dataflow_graph.edge(source.name, target.name, label=target.name, _attributes=rule_attributes)
        # print(dataflow_graph.pipe('svg').decode('utf-8'))
        return dataflow_graph.pipe('svg').decode('utf-8')

    def get_unused_dimensions():
        raise NotImplementedError('not supported')

    def get_server_name(self):

        with TM1Service(address=self.server_adress,
                        port=self.server_port,
                        user=self.server_user,
                        password=self.server_password,
                        ssl=True) as tm1:
            return tm1.server.get_server_name()

    def get_process_overview(self):
        with TM1Service(address=self.server_adress,
                        port=self.server_port,
                        user=self.server_user,
                        password=self.server_password,
                        ssl=True) as tm1:
            log = tm1.server.get_message_log_entries()

            process_names = pd.DataFrame.from_records([[process.name, True] for process in self.processes])
            process_names = process_names.set_index(0)
            process_names = process_names.rename(columns={1: 'process_exists'})

            # TODO: horrible horrible things, make it go away!
            df = pd.DataFrame.from_records(log)
            process_log = df[df.Logger == 'TM1.Process']
            process_log.head()
            process_name = process_log['Message'].str.extract('"([^"]*)"').rename(columns={0: "process_name"})
            process_duration = process_log['Message'].str.extract('([0-9]*\.[0-9]*)').rename(
                columns={0: "process_duration"})
            # process_log['process_name']
            process_log = process_log.join(process_name)
            process_log = process_log.join(process_duration)
            # drop non runtime related
            process_log = process_log[
                (process_log.process_name.notnull()) & (process_log.process_duration.notnull()) & (
                        process_log['Level'] == 'Info')]
            # process_log['process_duration'] = pd.to_numeric(process_log['process_duration'])#

            last_runs = process_log.groupby('process_name').tail(7)
            last_runs['process_duration'] = pd.to_numeric(last_runs['process_duration'])
            metrics = last_runs.groupby('process_name')['process_duration'].mean()
            # metrics = metrics.rename(columns={"process_duration": "Average Duration"})

            last_run = last_runs.groupby('process_name').tail(1)
            last_run = last_run.set_index('process_name')
            last_run = last_run.rename(columns={"process_duration": "Last duration", "TimeStamp": 'Last successful run'})
            # last_run =
            metrics = pd.concat([metrics, last_run], axis=1, join_axes=[metrics.index])
            metrics = metrics.join(process_names, how='outer')
            metrics = metrics.reset_index()
            metrics = metrics.rename(columns={"process_duration": "Average duration", 'index': 'Process name'})
            metrics = metrics[
                ['Process name', 'Average duration', 'Last duration', 'Last successful run', 'process_exists']]
            metrics = metrics.round({'Average duration': 1, 'Last duration':1})
            metrics = metrics.fillna('-')

        return metrics.to_dict('records')

    def call_api(self, call_method):
        """ calls REST API with method

        ToDo: implement Certificate and reenable CERT checking

        """
        rest_call = 'https://' + self.server_adress + ':' + self.server_port + '/api/v1/' + call_method

        call_result = requests.get(rest_call, auth=(self.server_user, self.server_password),
                                   verify=self.ssl_verify)
        if (call_result.ok):
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

    def get_tm1object_by_type_and_name(self, object_type, object_name, create_object=False):
        tm1_object = None
        if object_type == 'None':
            tm1_object = None
        elif object_type == 'ODBC':
            tm1_object = self.get_object_by_name_from_list(object_name, self.odbcs)
            if tm1_object is None and create_object:
                tm1_object = ODBC(object_name)
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
                tm1_object = Text(object_name)
                self.texts.append(tm1_object)
        return tm1_object

    def __fetch_processes(self):
        call_method = 'Processes'
        processes = self.call_api(call_method)
        self.processes = []
        for process_json in processes:
            process = Process(process_json, self)
            self.processes.append(process)

    def __fetch_dimensions(self):
        call_method = 'Dimensions'
        dimensions = self.call_api(call_method)
        self.dimensions = []
        for dimension_json in dimensions:
            dimension = Dimension(dimension_json, self)
            self.dimensions.append(dimension)

    def __fetch_cubes(self):
        call_method = 'Cubes?$expand=Dimensions'
        cubes = self.call_api(call_method)
        self.cubes = []
        for cube_json in cubes:
            cube = Cube(cube_json, self)
            self.cubes.append(cube)

    def __fetch_rules(self):
        call_method = 'Cubes'
        rules = self.call_api(call_method)
        self.rules = []
        for rule_json in rules:
            if rule_json['Rules'] != None:
                rule = Rule(rule_json, self)
                self.rules.append(rule)

    def get_Configuration(self):
        # get via api
        # or get from cfg file
        raise NotImplementedError('not supported')

    def get_rules():
        raise NotImplementedError('not supported')

    def get_cubes():
        raise NotImplementedError('not supported')

    def get_dimensions():
        raise NotImplementedError('not supported')
