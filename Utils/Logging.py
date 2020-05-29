import logging.config
import os

import yaml


def setup_logging(
        default_path='logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        try:
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
        except Exception as e:
            print(e)
            print("Error in logging config. Using default configs")
            logging.basicConfig(level=default_level)

    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs')

    logging.getLogger('discord').setLevel(logging.WARNING)
