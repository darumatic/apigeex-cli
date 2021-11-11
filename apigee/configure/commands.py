import configparser
import sys

import click
from click_aliases import ClickAliasedGroup

from apigee import APIGEE_CLI_CREDENTIALS_FILE, APIGEE_CLI_DIRECTORY
from apigee.utils import make_dirs


class HiddenSecret(object):
    def __init__(self, secret=''):
        self.secret = secret

    def __str__(self):
        return '*' * 16 if self.secret else ''


KEY_LIST = ('username', 'token', 'org',)
config = configparser.ConfigParser()
config.read(APIGEE_CLI_CREDENTIALS_FILE)
profile = 'default'

for i, arg in enumerate(sys.argv):
    if arg == '-P' or arg == '--profile':
        try:
            profile = sys.argv[i + 1]
        except IndexError:
            pass
try:
    profile_dict = dict(config._sections[profile])
    for key in KEY_LIST:
        if key not in profile_dict:
            profile_dict[key] = ''
except KeyError:
    profile_dict = {k: '' for k in KEY_LIST}

# @click.group(cls=ClickAliasedGroup)
# @click.command(aliases=['conf', 'config', 'cfg'])
@click.command(help='Configure Apigee X credentials.')
@click.option(
    '-u',
    '--username',
    prompt='Apigee username (email)',
    default=profile_dict['username'],
    show_default=True,
)
@click.option(
    '--token',
    default=profile_dict['token'],
    help='specify GCP OAuth Token',
    prompt='GCP OAuth Token',
    show_default=False,
)
@click.option(
    '-o',
    '--org',
    prompt='Default Apigee organization (recommended)',
    default=profile_dict['org'],
    show_default=True,
)
@click.option(
    '-P',
    '--profile',
    help='name of the user profile to create/update',
    default='default',
    show_default=True,
)
def configure(username, token, org, profile):
    if isinstance(token, HiddenSecret):
        token = token.secret
    profile_dict['username'] = username
    profile_dict['token'] = token
    profile_dict['org'] = org
    config[profile] = {k: v for k, v in profile_dict.items() if v}
    make_dirs(APIGEE_CLI_DIRECTORY)
    with open(APIGEE_CLI_CREDENTIALS_FILE, 'w') as cf:
        config.write(cf)
