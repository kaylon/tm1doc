import re
import TM1Object
from config import *
# import myutils

class Process(TM1Object.TM1Object):
    """docstring for """
    def __init__(self, json, server):
        self.server = server
        self.json = json
        self.name = json['Name']
        #source
        self.data_sources = []
        self.fetch_data_sources()
        # code
        self.prolog = json['PrologProcedure']
        self.metadata = json['MetadataProcedure']
        self.data = json['DataProcedure']
        self.epilog = json['EpilogProcedure']
        # target
        self.data_targets = []
        self.fetch_data_targets()


    def fetch_data_sources(self):
        self.data_sources = []
        # processes only has one or no source
        data_source_type = self.json['DataSource']['Type']
        data_source_name = 'None'
        if data_source_type == 'None':
            data_source_name = 'None'
        elif data_source_type == 'ODBC':
            data_source_name = self.json['DataSource']['dataSourceNameForServer']
            data_source_name += '.' + self.get_ODBC_Table_Name(self.json['DataSource']['query'])
        elif data_source_type == 'ASCII':
            data_source_type = 'Text'
            data_source_name = self.json['DataSource']['dataSourceNameForServer']
        elif data_source_type == 'TM1CubeView':
            # don't muck around with modeling views and skip to cubes!
            data_source_type = 'Cube'
            data_source_name = self.json['DataSource']['dataSourceNameForServer']
        if data_source_type[:1] != data_source_type[:1].capitalize():
            data_source_type = data_source_type.capitalize()
        tm1_object = self.server.get_tm1object_by_type_and_name(data_source_type, data_source_name, create_object = True)
        if tm1_object != None:
            self.data_sources.append(tm1_object)

    def fetch_data_targets(self):
        """ ToDo: improve support for different coding styles """
        self.data_targets = []
        # data can only be written in the data tab, don't fuck with tm1s case insensitivity madness
        data = self.data.lower()
        # strip all chars apart from alphanumeric ones and hyphens
        stripped_data = re.sub('[^0-9a-zA-Z\']', ' ', data)
        # look for cellputn or cellincrement n
        # some regex magician might be able to do that way more efficiently!
        words = stripped_data.split()
        for i in range(len(words)):
            word = words[i]
            if word in ['cellincrementn', 'cellputn']:
                # expect 'cellputn( vValue, 'Sales' ' in original data
                # looks like 'cellputn  vValue  'Sales' ' in stripped data
                cube = words[i+2]
                # try to find variable assignment in case cube nome is not passed in as string!
                if cube[0] == '\'':
                    cube_handle = self.server.get_tm1object_by_type_and_name('Cube', cube.capitalize())
                    if cube_handle != None:
                        self.data_targets.append(cube_handle)
                else:
                    cube_name = self.find_constant_assignment(cube).capitalize()
                    cube_handle = self.server.get_tm1object_by_type_and_name('Cube', cube_name)
                    if cube_handle != None:
                        self.data_targets.append(cube_handle)


    def find_constant_assignment(self, variable):
        prolog = self.prolog.lower()
        pattern = variable  + '.*=.*\'.*\';'
        match = re.search(pattern, prolog)
        if match != None:
            pattern = '(?<=\').*(?=\')'
            assignment = prolog[match.start():match.end()]
            match = re.search(pattern, assignment)
            cube_name = assignment[match.start():match.end()]
        else:
            # comment out the next line if you don't care and just want it to run
            raise NotImplementedError( 'Could not find Cube name in' + self.name + ' for variable name: '+  variable)
            cube_name = ''
        return cube_name

    #
    # def get_data_target_type(self):
    #     # only filename as indicator for now
    #     end_position = self.name.find('.')
    #     # print(self.process_name[0:end_position].title())
    #     return(self.name[0:end_position].title())

    def get_ODBC_Table_Name(self, query):
        """ extract table name from simple (no join) sql select statement"""
        pattern = 'FROM\s+\S+'
        res = re.search(pattern, query.upper())
        source = res.group(0).replace('[', '')
        source = source.replace(']', '')
        source = source.replace('FROM', '')
        source = source.replace(' ', '')
        return(source)
    #
    # def get_data_target(self):
    #     # use filename as indication for target
    #     position_of_first_point = self.name.find('.')+1
    #     position_of_second_point = self.name.find('.',      position_of_first_point)
    #     # print (position_of_first_point, position_of_second_point)
    #     return(self.name[position_of_first_point:position_of_second_point].title())
