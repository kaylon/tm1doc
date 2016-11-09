
from tm1doc import TM1Object

class Text(TM1Object.TM1Object):
    """docstring for """
    def __init__(self, name):
        super(Text, self).__init__(name)

    def get_name(self):
        return self.name
