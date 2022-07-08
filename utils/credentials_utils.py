from configparser import ConfigParser, SectionProxy
import logging
import re
from typing import Optional, Tuple

from utils.config_utils import read_config


def get_credentials_from_user() -> ConfigParser:
    logging.info("Please, paste the credentials file block:")

    no_of_lines = 4
    lines = []
    for i in range(no_of_lines):
        lines.append(input())

    return read_config("\n".join(lines), is_string=True)


def process_credentials_block() -> Tuple[Optional[SectionProxy], Optional[str]]:
    raw_user_credentials = get_credentials_from_user()
    account_role_name = raw_user_credentials.sections()[0]
    user_credentials = raw_user_credentials[account_role_name]
    logging.info(f"Obtained credentials for account-role [{account_role_name}]")

    return user_credentials, account_role_name


def get_profile_name_from_user(account_role_name: str) -> str:
    account, role = account_role_name.split("_")
    role_snake = re.sub(r'(?<!^)(?=[A-Z])', "-", role).lower()
    profile = f"{role_snake}-{account}"
    logging.info(f"Write a name for the new profile: ({profile})")
    user_input = input()
    return user_input if user_input != "" else profile


def get_profile_region_from_user(default_profile_region: str) -> str:
    logging.info(f"Which region do you use as default for this account? [{default_profile_region}]")
    user_input = input()
    return user_input if user_input != "" else default_profile_region
