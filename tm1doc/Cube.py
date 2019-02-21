
from tm1doc.TM1Object import TM1Object

class Cube(TM1Object):
    """docstring for """
    def __init__(self, json, server):
        # super(Cube, self).__init__(cube_name)
        self.server = server
        self.json = json
        self.name = json['Name']
        self.dimensions = []
        self.fetch_dimensions()

    def fetch_dimensions(self):
        for dimension_json in self.json['Dimensions']:
            dimension_name = dimension_json['Name']
            dimension = self.server.get_tm1object_by_type_and_name('Dimension', dimension_name)
            self.dimensions.append(dimension)

    def pretty_print(self):
        print(self.name)
        for dimension in self.dimensions:
            print('\t'+dimension.name)

    def get_cube_name(self):
        return self.cube_name
    def get_dimensions(self):
        raise NotImplementedError( 'not supported' )
