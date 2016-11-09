import re
import TM1Object

class Rule(TM1Object.TM1Object):
    """docstring for """
    def __init__(self, json, server):
        self.server = server
        self.name = json['Name']
        self.code = json['Rules']
        self.data_sources = []
        self.fetch_data_sources()
        self.data_targets = []
        self.fetch_data_targets()


    def fetch_data_targets(self):
        self.data_targets = []
        target_name = self.name
        target_type = 'Cube' # target is always the cube a rule is attached to
        target = self.server.get_tm1object_by_type_and_name(target_type, target_name)
        self.data_targets.append(target)

    def fetch_data_sources(self):
        """ parses rule code to obtain all sources in tm1 DB format """
        self.data_sources = []
        rule_code = self.code
        # ignore feeders
        feeders_start_position = rule_code.upper().find('FEEDERS;')
        rule_calculations = rule_code[0:feeders_start_position]
        # get DB rules
        # pattern = '\n\s*[^#].*=.*+.*DB.*;'
        pattern = '.*DB.*;'
        matches = re.findall(pattern, rule_calculations)

        for match in matches:
            position_of_DB = match.find('DB')
            posistion_of_first_hyphen = match.find('\'', position_of_DB) + 1
            posistion_of_second_hyphen = match.find('\'',posistion_of_first_hyphen )
            source_name = match[posistion_of_first_hyphen:posistion_of_second_hyphen]
            source_type = 'Cube' # DB function can only call on cubes afaik
            source = self.server.get_tm1object_by_type_and_name(source_type, source_name)
            if source not in self.data_sources:
                self.data_sources.append(source)
