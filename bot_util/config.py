from collections import namedtuple
import os


import yaml


HARD_CORDING_DEFAULT_CONFIG = dict()
YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }
if os.path.isfile('./data/default_config.yaml'):
    with open('./data/default_config.yaml')as f:
        raw_default_config = yaml.safe_load(f)
else:
    raw_default_config = HARD_CORDING_DEFAULT_CONFIG
    with open('./data/default_config.yaml','w')as f:
        yaml.dump(raw_default_config,f,**YAML_DUMP_CONFIG)

if os.path.isfile('./config.yaml'):
    with open('./config.yaml')as f:
        raw_config = yaml.safe_load(f)
else:
    raw_config = raw_default_config
    with open('./config.yaml','w')as f:
        yaml.dump(raw_config,f,**YAML_DUMP_CONFIG)

class default_config():
    pass

class config():
    pass
