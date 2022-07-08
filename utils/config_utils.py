import argparse
from configparser import ConfigParser
import logging
import os
from typing import Optional, Tuple


def get_module_config() -> Tuple[Optional[str], Optional[str]]:
    parser = argparse.ArgumentParser(description="Copy credentials block from AWS SSO to credentials file")
    parser.add_argument("-c", "--astc_config_path", help="Config location for astc module", default="~/.astc.cfg")
    parser.add_argument("-a", "--aws_config_path", help="AWS credentials location", default=None)
    args = parser.parse_args()

    return args.astc_config_path, args.aws_config_path


def read_config(config_file: str, is_string: bool = False) -> ConfigParser:
    config_parser = ConfigParser(allow_no_value=True)
    if is_string:
        config_parser.read_string(config_file)
        return config_parser

    with open(config_file) as file:
        config_parser.read_file(file)
        return config_parser


def write_config(config_parser: ConfigParser, config_parser_path: str):
    with open(config_parser_path, 'w') as configfile:
        config_parser.write(configfile)


def read_configuration_files(astc_config_path: str = "~/.astc.cfg", aws_config_path: str = None)\
        -> Tuple[Tuple[Optional[ConfigParser], Optional[str]], Tuple[Optional[ConfigParser], Optional[str]]]:
    user_home = os.path.expanduser("~")
    astc_config_extended_path = astc_config_path.replace("~", user_home)
    astc_config = read_config(astc_config_extended_path)

    aws_config_path = aws_config_path if aws_config_path else astc_config["aws_config"].get("credentials_file_path")
    aws_config_extended_path = aws_config_path.replace("~", user_home)
    aws_config = read_config(aws_config_extended_path)
    logging.info("Configuration and credentials files loaded")

    return (astc_config, astc_config_extended_path), (aws_config, aws_config_extended_path)