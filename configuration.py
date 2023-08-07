import configparser
import logging

logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config_structure = {
    'DISCORD': {
        'BOT_TOKEN': str,
    },
    'RIOT': {
        'API_KEY': str
    },
    'REDIS': {
        'HOST': str,
        'PORT': int,
        'DB': int,
    },
}


def read_config(config_path):
    if not config.read(config_path):
        logger.error(f"Could not load '{config_path}' configuration file")
        exit(1)

    success = True
    config_data = {}
    for section in config_structure:
        if section not in config:
            success = False
            logger.error(f"Section '{section}' not found in '{config_path}' file")

        config_section = config[section]
        section_data = {}
        for key, data_type in config_structure[section].items():
            if key not in config_section:
                success = False
                logger.error(f"Field '{key}' not found in '{section}' section of '{config_path}' file")
                continue

            try:
                section_data[key] = data_type(config_section[key])
            except ValueError:
                success = False
                logger.error(f"Field '{key}' in '{section}' section could not be read as '{data_type.__name__}'")

        config_data[section] = section_data
    if not success:
        raise Exception("Configuration is incomplete or incorrect")

    return config_data
