import os


import yaml


from . import logger


HARD_CORDING_DEFAULT_CONFIG = dict()
YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


class __Config:
    def __init__(self):
        self.__default_config = HARD_CORDING_DEFAULT_CONFIG

    @property
    def default_config(self):
        return self.__default_config

    @default_config.setter
    def default_config(self,value):
        if not isinstance(value,dict):
            raise TypeError(f'only set dict')
        self.__default_config = value

    def load_config(self):
        if not os.path.isdir('./data'):
            os.mkdir('./data')
            logger.warning(f'create data dirctory')

        if os.path.isfile('./data/default_config.yaml'):
            with open('./data/default_config.yaml')as f:
                self.default_config =  yaml.safe_load(f)
        else:
            logger.warning(f'create data/default_config.yaml file')
            with open('./data/default_config.yaml','w')as f:
                yaml.dump(self.default_config,f,**YAML_DUMP_CONFIG)

        if os.path.isfile('./config.yaml'):
            with open('./config.yaml')as f:
                config = yaml.safe_load(f)
        else:
            logger.warning(f'create config.yaml file')
            with open('./config.yaml','w')as f:
                yaml.dump(self.default_config,f,**YAML_DUMP_CONFIG)
            config = self.default_config

        return config


config = __Config()
