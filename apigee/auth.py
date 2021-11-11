import configparser
import json
import os
import sys
import click

from apigee import (APIGEE_CLI_CREDENTIALS_FILE,
                    APIGEE_CLI_DIRECTORY, APIGEE_CLI_IS_MACHINE_USER
                )
from apigee.cls import AliasedGroup
# from apigee.prefix import common_prefix_options
from apigee.prefix import auth_with_prefix as with_prefix
from apigee.types import Struct
from apigee.utils import make_dirs


def attach_username_option(func, profile):
    username = get_credential(profile, 'username')
    username_envvar = os.environ.get(f'APIGEE_USERNAME', '')
    if username:
        func = click.option('-u', '--username', default=username, show_default='current username')(
            func
        )
    elif username_envvar:
        func = click.option(
            '-u', '--username', default=username_envvar, show_default='current username'
        )(func)
    else:
        func = click.option('-u', '--username', required=True)(func)
    return func


def attach_token_option(func, profile):
    token = get_credential(profile, 'token')
    token_envvar = os.environ.get(f'APIGEE_TOKEN', '')
    if token:
        func = click.option('-t', '--token', default=token, show_default='current token')(
            func
        )
    elif token_envvar:
        func = click.option(
            '-t', '--token', default=token_envvar, show_default='current token'
        )(func)
    else:
        func = click.option('-t', '--token', required=True)(func)
    return func


def attach_org_option(func, profile):
    org = get_credential(profile, 'org')
    org_envvar = os.environ.get(f'APIGEE_ORG', '')
    if org:
        func = click.option('-o', '--org', default=org, show_default='current org')(func)
    elif org_envvar:
        func = click.option('-o', '--org', default=org_envvar, show_default='current org')(func)
    else:
        func = click.option('-o', '--org', required=True)(func)
    return func


def common_auth_options(func):
    profile = 'default'
    for i, arg in enumerate(sys.argv):
        if arg == '-P' or arg == '--profile':
            try:
                profile = sys.argv[i + 1]
            except IndexError:
                pass
    attach_username_option(func, profile)
    attach_token_option(func, profile)
    attach_org_option(func, profile)
    func = click.option(
        '-P',
        '--profile',
        help='name of the user profile to authenticate with',
        default=profile,
        show_default=True,
    )(func)
    return func


def gen_auth(username=None, token=None):
    return Struct(username=username, token=token)


def generate_auth_error_message(error):
    error_message = f'An exception of type {type(error).__name__} occurred. Arguments:\n{error}\nDouble check your credentials and try again.'
    if APIGEE_CLI_IS_MACHINE_USER:
        return f'{error_message} \nWARNING: APIGEE_CLI_IS_MACHINE_USER={APIGEE_CLI_IS_MACHINE_USER}'
    return error_message


def get_credential(section, key):
    try:
        config = configparser.ConfigParser()
        config.read(APIGEE_CLI_CREDENTIALS_FILE)
        if section in config:
            return config[section][key]
    except:
        return


def set_header(auth_obj, headers={}):
    if auth_obj.token:
        headers['Authorization'] = f'Bearer {auth_obj.token}'
    else:
        raise Exception("GCP OAuth Token must be set")
    return headers


def auth_with_prefix(auth_obj, org, name, file=None, key='name'):
    if file:
        with open(file) as f:
            attr = json.loads(f.read())[key]
        return with_prefix(auth_obj, org, attr)
    return with_prefix(auth_obj, org, name)


@click.command(
    help='Custom authorization commands. More information on the use cases for these commands are yet to be documented.',
    cls=AliasedGroup,
)
def auth():
    pass

