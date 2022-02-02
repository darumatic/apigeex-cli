import click

from apigee import console
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.references.references import References
from apigee.silent import common_silent_options
from apigee.verbose import common_verbose_options


@click.group(help='References in an organization and environment.')
def references():
    pass


def _list_all_references(
    username,
    token,
    org,
    profile,
    environment,
    **kwargs
):
    return References(
        gen_auth(username, token), org, None
    ).list_all_references(environment)


@references.command(help='List all references in an organization and environment.')
@common_auth_options
@common_prefix_options
@common_silent_options
@common_verbose_options
@click.option('-e', '--environment', help='environment', required=True)
def list(*args, **kwargs):
    console.echo(_list_all_references(*args, **kwargs))


def _get_reference(
    username, token, org, profile, name, environment, **kwargs
):
    return (
        References(gen_auth(username, token), org, name)
        .get_reference(environment)
        .text
    )


@references.command(help='Get reference in an organization and environment.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='reference name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
def get(*args, **kwargs):
    console.echo(_get_reference(*args, **kwargs))


def _delete_reference(
    username, token, org, profile, name, environment, **kwargs
):
    return (
        References(gen_auth(username, token), org, name)
        .delete_reference(environment)
        .text
    )


@references.command(help='Delete a reference')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='reference name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
def delete(*args, **kwargs):
    console.echo(_delete_reference(*args, **kwargs))


def _create_reference(
    username,
    token,
    org,
    profile,
    name,
    environment,
    description,
    resource_type,
    refers,
    **kwargs
):
    return (
        References(gen_auth(username, token), org, name)
        .create_reference(environment, description, resource_type, refers)
        .text
    )


@references.command(help='Create a reference. References must refer to a keystore that also exists in the parent environment.')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='reference name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-d', '--description', help='description', default=None)
@click.option('-t', '--resource-type', help='resource type', required=True, type=click.Choice(["KeyStore", "TrustStore"]))
@click.option('-r', '--refers', help='The id of the resource to which this reference refers', required=True)
def create(*args, **kwargs):
   console.echo( _create_reference(*args, **kwargs))


def _update_reference(
    username,
    token,
    org,
    profile,
    name,
    environment,
    description,
    resource_type,
    refers,
    **kwargs
):
    return (
        References(gen_auth(username, token), org, name)
        .update_reference(environment, description, resource_type, refers)
        .text
    )


@references.command(help='Update an existing reference')
@common_auth_options
@common_silent_options
@common_verbose_options
@click.option('-n', '--name', help='reference name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-d', '--description', help='description', default=None)
@click.option('-t', '--resource-type', help='resource type', required=True, type=click.Choice(["KeyStore", "TrustStore"]))
@click.option('-r', '--refers', help='The id of the resource to which this reference refers', required=True)
def update(*args, **kwargs):
    console.echo(_update_reference(*args, **kwargs))
