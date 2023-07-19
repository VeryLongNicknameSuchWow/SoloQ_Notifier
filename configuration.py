import configparser
import logging

logger = logging.getLogger("configuration")

config = configparser.ConfigParser()
config_structure = {
    'DISCORD': [
        'BOT_TOKEN',
    ],
    'RIOT': [
        'API_KEY',
    ],
    'MONGO': [
        'DB_USER',
        'DB_PASSWORD',
        'DB_HOST',
        'DB_PORT',
        'DATABASE',
    ],
}


def read_config(config_path):
    if not config.read(config_path):
        logger.error(f"Could not load '{config_path}' configuration file")
        exit(1)

    success = True
    for section in config_structure:
        if section not in config:
            success = False
            logger.error(f"Section '{section}' not found in '{config_path}' file")

        config_section = config[section]
        for key in config_structure[section]:
            if key not in config_section:
                success = False
                logger.error(f"Field '{key}' not found in '{section}' section of '{config_path}' file")

    if not success:
        raise Exception("Configuration is incomplete")

    return config
