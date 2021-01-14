from .code_generator import code_generator
import argparse

class script_generator_settings:
    def __init__(self, engine_name):
        self.engine_name = engine_name
        self.__keys = []
        self.__setting_strs = dict()
        self.__defaults = dict()
        self.__flags = dict()
        self.__helps = dict()

    def add_setting_key(self, key, setting_str, default, flag, help_str):
        '''
        Add one setting key to the setting object
        '''
        self.__keys.append(key)
        self.__setting_strs[key] = setting_str
        self.__defaults[key] = default
        self.__flags[key] = flag
        self.__helps[key] = help_str
    
    def load_from_dict(self, setting_dict):
        '''
        load settings from json str

        Keyword Arguments:
        setting_dict - dictionary containing keys as key names, and 
                       values as dictionary containing setting_str, 
                       defaults and flag.

        >>> sample_setting = script_generator_settings('sampleGenerator')
        >>> sample_dict = {'sample_setting': {'setting_str': 'setting: <setting>', 'default': 1, 'flag': '-s', 'help': 'help'}}
        >>> sample_setting.load_from_dict(sample_dict)
        >>> sample_setting.get_setting_str('sample_setting')
        'setting: <setting>'
        >>> sample_setting.get_default('sample_setting')
        1
        '''
        for key, value in setting_dict.items():
            self.add_setting_key(key, value['setting_str'], value['default'], value['flag'], value['help'])
    
    def get_default(self, key):
        '''
        Return the default value of an option

        Keyword Arguments:
        key - the key of which the default value is returned
        '''
        return self.__defaults[key]

    def get_setting_str(self, key):
        '''
        Return the setting string of an option

        Keyword Arguments:
        key - the key of which the setting string is returned
        '''
        return self.__setting_strs[key]
    
    def get_help(self,key):
        '''
        Return the helper string of an option

        Keyword Arguments:
        key - the key of which the helper string is returned
        '''
        return self.__helps[key]
        
    def get_flag(self,key):
        '''
        Return the flag of an option

        Keyword Arguments:
        key - the key of which the flag is returned
        '''
        return self.__flags[key]
    
    def get_keys(self):
        '''
        Return the keys in a setting object
        '''
        return self.__keys

class script_generator:
    def __init__(self, eigen_name, setting_dict, sub_dict):
        self.__settings = script_generator_settings(eigen_name)
        self.load_setting_from_dict(setting_dict)
        self.template = ''
        self.template_substitution_dict = sub_dict

    def load_template(self, template):
        '''
        Load the template

        Keyword Arguments:
        template - of string type, the template
        sub_dict - dictionary of substitution groups
        '''
        self.template = template


    def set_argparser(self, parser):
        '''
        Set the argument parser for the script generator

        Keyword Arguments:
        parser - a subcommand parser for argparse library
        '''
        for key in self.__settings.get_keys():
            parser.add_argument('--' + key, 
                                self.__settings.get_flag(key), 
                                help=self.__settings.get_help(key), 
                                dest=key, 
                                default=self.__settings.get_default(key), 
                                )
        
        for key, value in self.template_substitution_dict.items():
            parser.add_argument('--' + value, 
                                help='contents to substitute ' + key.__str__())

    def load_setting_from_dict(self, setting_dict):
        '''
        load the settings from a python dictionary

        Keyword Arguments:
        setting_dict - a python dictionary containing necessary settings
        '''
        self.__settings.load_from_dict(setting_dict)
    
    def render(self, arg_dict):
        '''
        Render the text according to the args
        '''
        code = code_generator(indent_level=0, indent_str='    ')

        header_block = code.add_block()
        code.add_line('')
        body_block = code.add_block()

        for key in self.__settings.get_keys():
            header_block.add_line(self.__settings.get_setting_str(key).replace('<setting>', arg_dict[key].__str__()))

        template = self.template

        for key, value in self.template_substitution_dict.items():
            template = template.replace(key, arg_dict[value].__str__())
        
        body_block.add_line(template)
        
        return code.__str__()
