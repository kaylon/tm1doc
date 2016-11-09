class TM1Object(object):
    """docstring for """
    def __init__(self, name):
        # super(, self).__init__()
        self.name = name



    def get_class_name(self):
        return(type(self).__name__)

    def get_object_name(self):
        return(self.name)
