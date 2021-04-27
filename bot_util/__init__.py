import logging


YAML_DUMP_CONFIG = {
    'encoding':'utf8',
    'allow_unicode':True,
    'default_flow_style':False
    }


logging.getLogger(__name__).addHandler(logging.NullHandler())
