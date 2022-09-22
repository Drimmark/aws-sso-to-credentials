from configparser import ConfigParser, SectionProxy
import logging

from utils.config_utils import get_module_config, read_configuration_files, write_config
from utils.credentials_utils import (
    get_profile_name_from_user,
    get_profile_region_from_user,
    process_credentials_block,
)

logging.basicConfig(level=logging.DEBUG)


def get_confirmation_from_user() -> bool:
    user_input = input()
    return user_input.lower() in ["y", "yes"]


def process_profile(
    astc_config: ConfigParser,
    astc_config_extended_path: str,
    aws_credentials: ConfigParser,
    aws_config_extended_path: str,
    user_credentials: SectionProxy,
    account_role_name: str,
):
    profile_name = astc_config["profile_account_mapping"].get(account_role_name)
    if not profile_name:
        logging.error(f"Account-role [{account_role_name}] not found in astc config file")
        logging.info("Do you want to create the account-role mapping? (y/yes)")
        if not get_confirmation_from_user():
            exit()
        profile_name = get_profile_name_from_user(account_role_name)
        astc_config["profile_account_mapping"][account_role_name] = profile_name
        write_config(astc_config, astc_config_extended_path)

    logging.info(f"Obtained profile [{profile_name}] from account-role [{account_role_name}]")
    if profile_name not in aws_credentials.sections():
        logging.error(f"Profile [{profile_name}] not found in credentials file")
        logging.info("Do you want to add the profile? (y/yes)")
        if not get_confirmation_from_user():
            exit()
        aws_credentials[profile_name] = {}

    logging.info(f"Setting credentials for profile [{profile_name}]")
    for option in user_credentials:
        aws_credentials[profile_name][option] = user_credentials[option]

    logging.info(
        f"""Do you want to update default region (current: {aws_credentials[profile_name].get('region', 'None')})? (y/yes)"""  # noqa: E501
    )
    if get_confirmation_from_user():
        default_profile = (
            aws_credentials[profile_name].get("region")
            if "region" in aws_credentials[profile_name]
            else astc_config["aws_config"].get("default_profile", "eu-west-1")
        )
        profile_region = get_profile_region_from_user(default_profile)
        aws_credentials[profile_name]["region"] = profile_region

    write_config(aws_credentials, aws_config_extended_path)
    logging.info(f"Credentials for profile [{profile_name}] setted in credentials config ({aws_config_extended_path})")


def main(astc_config_path: str, aws_credentials_path: str):
    (astc_config_file, astc_config_extended_path_file), (
        aws_credentials_file,
        aws_config_extended_path_file,
    ) = read_configuration_files(astc_config_path, aws_credentials_path)

    ask_again = True
    while ask_again:
        user_credentials_block, account_role_name_block = process_credentials_block()

        process_profile(
            astc_config_file,
            astc_config_extended_path_file,
            aws_credentials_file,
            aws_config_extended_path_file,
            user_credentials_block,
            account_role_name_block,
        )

        logging.info("Do you want to introduce new credentials? (y/yes)")
        ask_again = get_confirmation_from_user()


if __name__ == "__main__":
    module_astc_config_path, module_aws_credentials_path = get_module_config()
    main(module_astc_config_path, module_aws_credentials_path)
