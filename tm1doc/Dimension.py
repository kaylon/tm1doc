
from tm1doc.TM1Object import TM1Object

class Dimension(TM1Object):
    """docstring for """
    def __init__(self, json, server):
        # super(Dimension, self).__init__(dimension_name)
        self.server = server
        self.name = json['Name']

        #
        # self.cube_name = cube_name

    def get_name(self):
        return self.name
