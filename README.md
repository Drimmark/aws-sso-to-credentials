# AWS SSO to credentials

This module need a configuration file that need to be stored in "`~/.astc.cfg`". If the module config is located in
other path, the module need to be invoked using `astc -c <astc-config-location>`. 

Example of `~/.astc.cfg` file:
```cfg
[aws_config]
credentials_file_path = ~/.aws/credentials
default_profile = eu-west-1

[profile_account_mapping]
<ugly_aws_sso_name> = <awesome_config_name>