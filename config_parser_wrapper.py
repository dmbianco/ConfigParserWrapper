import configparser
import re
import ast

# ast is used for parsing dictionaries that are pickled as strings. It usually infers
# types of the values correctly.

def boolean_parser(string):
    '''
    It parses a string looking for a boolean interpretable value
    '''
    string = str.lower(string)
    if string in ['true', '1', 't', 'y', 'yes']:
        return True
    elif string in ['false', '0', 'f', 'n', 'no']:
        return False
    else:
        return string


class ConfigParserWrapper:
    '''
    The recognized/supported types are defined into the _types dictionrary.
    The regex _extract_type extracts the type of a varible from Python output,
    e.g. "<type 'int'>".
    The regex _get_type extracts the type of a restored variable since it is saved
    following the pattern "type_name".
    '''
    _types = {"int":int, "float":float, "dict":ast.literal_eval, "str":str,
            "bool":boolean_parser}
    _extract_type = re.compile("'(.+)'>$")
    _get_type = re.compile("^([^_]+)")
    

    def __init__(self, dic={}):
        '''
        Constructor. The keys of dic should be sections and its values should be
        dictionaries of configuration variables.
        '''
        self.dic = dic
    

    def add_section_dict(self, dic_of_variables, section_name, check_section=True):
        '''
        It adds the dictionary dic_of_variables to self.dic with the key section_name.
        '''
        if section_name not in self.dic or not check_section:
            self.dic[section_name] = dic_of_variables
        else:
            print "{} already stored!"
    

    def save_config(self, output_file="parameters.cfg"):
        '''
        It saves the configurations.
        '''
        config = configparser.RawConfigParser()
        for section,dic_of_variables in self.dic.iteritems():
            config.add_section(section)
            for var,value in dic_of_variables.iteritems():
                type_of_var = str(type(value))
                type_of_var = re.findall(self._extract_type, type_of_var)[0]
                config.set(str(section), str(type_of_var) + "_" + str(var),str(value))

        with open(output_file, 'wb') as configfile:
            config.write(configfile)


    def load_config(self, input_file="parameters.cfg", flatten=False):
        '''
        It restores the configuration variables from a file. If flatten is true, 
        then the hierarchy section:dict_of_variables is flattened and all variables 
        are saved in the same dictionary; notice that homonymous variables could
        lead to unintended results in this case.
        '''
        config = ConfigParser.ConfigParser()
        config.read(input_file)

        all_configs = {}
        for section in config.sections():
            if not flatten:
                all_configs[section] = {}
                for var,value in dict(config.items(section)).iteritems():
                    all_configs[section].update(dict([self._parse_value(var,value)]))
            else:
                for var,value in dict(config.items(section)).iteritems():
                    all_configs.update(dict([self._parse_value(var,value)]))
        self.dict_of_configs = all_configs


    def _parse_value(self, variable, value):
        '''
        It parses the name of a saved variable that is in the form "type_name" and
        returns only its name and the cast value.
        '''
        var_type = re.findall(self._get_type, variable)[0]
        variable = re.sub(self._get_type, "", variable, 1)[1:]
        converter = None
        if var_type in self._types:
            converter = self._types[var_type]
            
        if converter:
            return variable, converter(value)
        else:
            print "{} is UNsupported! Returning a string for {}.".format(var_type, variable)
            return variable, value




