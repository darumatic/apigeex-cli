import click
from click_option_group import MutuallyExclusiveOptionGroup, optgroup

from apigee import console
from apigee.apis.apis import Apis
from apigee.apis.deploy import deploy as deploy_tool
from apigee.auth import common_auth_options, gen_auth
from apigee.prefix import common_prefix_options
from apigee.silent import common_silent_options
from apigee.types import Struct
from apigee.verbose import common_verbose_options


@click.group(
    help='The proxy APIs let you perform operations on API proxies, such as create, delete, update, and deploy.'
)
def apis():
    pass


def _delete_api_proxy_revision(
    username, token, org, profile, name, revision_number, **kwargs
):
    return (
        Apis(gen_auth(username, token), org)
        .delete_api_proxy_revision(name, revision_number)
        .text
    )


@apis.command(
    help='Deletes a revision of an API proxy and all policies, resources, endpoints, and revisions associated with it. The API proxy revision must be undeployed before you can delete it.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def delete_revision(*args, **kwargs):
    console.echo(_delete_api_proxy_revision(*args, **kwargs))


def _deploy_api_proxy_revision(
    username,
    token,
    org,
    profile,
    name,
    environment,
    revision_number,
    service_account,
    override=False,
    sequenced_rollout=False,
    **kwargs,
):
    return (
        Apis(gen_auth(username, token), org)
        .deploy_api_proxy_revision(
            name, environment, revision_number, service_account, override=override, sequenced_rollout=sequenced_rollout
        )
        .text
    )


@apis.command(
    help='Deploys a revision of an existing API proxy to an environment in an organization.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
@click.option('-a', '--service-account', help='Google Cloud IAM service account', required=True)
@click.option(
    '--override/--no-override',
    default=False,
    help='Flag that specifies whether to use seamless deployment to ensure zero downtime. Set this flag to "true" to instruct Edge to deploy the new revision fully before undeploying the existing revision.',
)
@click.option(
    '--sequenced-rollout/--no-sequenced-rollout',
    default=False,
    help="If set to true, a best-effort attempt will be made to roll out the routing rules corresponding to this deployment and the environment changes to add this deployment in a safe order.",
)
def deploy_revision(*args, **kwargs):
    console.echo(_deploy_api_proxy_revision(*args, **kwargs))


def _delete_undeployed_revisions(
    username,
    token,
    org,
    profile,
    name,
    save_last=0,
    dry_run=False,
    **kwargs,
):
    return Apis(
        gen_auth(username, token), org
    ).delete_undeployed_revisions(name, save_last=save_last, dry_run=dry_run)


@apis.command(
    help='Deletes all undeployed revisions of an API proxy and all policies, resources, endpoints, and revisions associated with it.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option(
    '--save-last',
    type=click.INT,
    help='denotes not to delete the N most recent revisions',
    default=0,
)
@click.option(
    '--dry-run/--no-dry-run', default=False, help='show revisions to be deleted but do not delete'
)
def clean(*args, **kwargs):
    _delete_undeployed_revisions(*args, **kwargs)


def _export_api_proxy(
    username,
    token,
    org,
    profile,
    name,
    revision_number,
    fs_write=True,
    output_file=None,
    **kwargs,
):
    return Apis(gen_auth(username, token), org).export_api_proxy(
        name,
        revision_number,
        fs_write=fs_write,
        output_file=output_file if output_file else f'{name}.zip',
    )


@apis.command(
    help='Outputs an API proxy revision as a ZIP formatted bundle of code and config files. This enables local configuration and development, including attachment of policies and scripts.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
@click.option(
    '-O', '--output-file', help='specify output file (defaults to API_NAME.zip)', default=None
)
def export(*args, **kwargs):
    _export_api_proxy(*args, **kwargs)


def _get_api_proxy(username, token, org, profile, name, **kwargs):
    return (
        Apis(gen_auth(username, token), org)
        .get_api_proxy(name)
        .text
    )


@apis.command(
    help='Gets an API proxy by name, including a list of existing revisions of the proxy.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
def get(*args, **kwargs):
    console.echo(_get_api_proxy(*args, **kwargs))


def _list_api_proxies(
    username,
    token,
    org,
    profile,
    format='json',
    **kwargs,
):
    return Apis(gen_auth(username, token), org).list_api_proxies(format=format)


@apis.command(
    help='Gets the names of all API proxies in an organization. The names correspond to the names defined in the configuration files for each API proxy.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@common_prefix_options
def list(*args, **kwargs):
    console.echo(_list_api_proxies(*args, **kwargs))


def _list_api_proxy_revisions(
    username, token, org, profile, name, **kwargs
):
    return (
        Apis(gen_auth(username, token), org)
        .list_api_proxy_revisions(name)
        .text
    )


@apis.command(help='List all revisions for an API proxy.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
def list_revisions(*args, **kwargs):
    console.echo(_list_api_proxy_revisions(*args, **kwargs))


def _undeploy_api_proxy_revision(
    username,
    token,
    org,
    profile,
    name,
    environment,
    revision_number,
    **kwargs,
):
    return (
        Apis(gen_auth(username, token), org)
        .undeploy_api_proxy_revision(name, environment, revision_number)
        .text
    )


@apis.command(help='Undeploys an API proxy revision from an environment.')
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
def undeploy_revision(*args, **kwargs):
    console.echo(_undeploy_api_proxy_revision(*args, **kwargs))


def _pull(
    username,
    token,
    org,
    profile,
    name,
    revision_number,
    environment,
    work_tree,
    dependencies=[],
    force=False,
    **kwargs,
):
    return Apis(
        gen_auth(username, token),
        org,
        revision_number,
        environment,
        work_tree=work_tree,
    ).pull(name, dependencies=dependencies, force=force)


@apis.command(
    help='Downloads an API proxy revision, along with any referenced key/value maps, target servers and caches into the current working directory.'
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-n', '--name', help='name', required=True)
@click.option('-r', '--revision-number', type=click.INT, help='revision number', required=True)
@click.option('-e', '--environment', help='environment', required=True)
@click.option(
    '--work-tree', help='set the path to the working tree (defaults to current working directory)'
)
@click.option('--force/--no-force', '-f/-F', default=False, help='force write files')
def pull(*args, **kwargs):
    _pull(*args, **kwargs)


def _deploy(
    username,
    token,
    org,
    profile,
    environment,
    name,
    service_account,
    directory,
    import_only,
    seamless_deploy,
    **kwargs,
):
    return deploy_tool(
        Struct(
            username=username,
            directory=directory,
            org=org,
            name=name,
            environment=environment,
            import_only=import_only,
            seamless_deploy=seamless_deploy,
            service_account=service_account,
            token=token
        )
    )


@apis.command(
    help="""Deploy APIs using an improved version of the Apigee API Proxy Deploy Tool: https://github.com/apigee/api-platform-samples/tree/master/tools

\b
   =========================================================================
   ==  NOTICE file corresponding to the section 4 d of                    ==
   ==  the Apache License, Version 2.0,                                   ==
   ==  in this case for the Apigee API Proxy Deploy Tool code.            ==
   =========================================================================

Apigee API Proxy Deploy Tool
https://github.com/apigee/api-platform-samples/tree/master/tools
These files are Copyright 2015 Apigee Corporation, released under the Apache2 License.
"""
)
@common_auth_options
@common_verbose_options
@common_silent_options
@click.option('-e', '--environment', help='environment', required=True)
@click.option('-n', '--name', help='name', required=True)
@click.option('-a', '--service-account', help='Google Cloud IAM service account', required=True)
@click.option(
    '-d',
    '--directory',
    help='directory with the apiproxy/ bundle',
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=False),
    required=True,
)
@optgroup.group(
    'Deployment options', cls=MutuallyExclusiveOptionGroup, help='The deployment options'
)
@optgroup.option(
    '--import-only/--no-import-only', '-i/-I', default=False, help='import only and not deploy'
)
@optgroup.option(
    '--seamless-deploy/--no-seamless-deploy',
    '-s/-S',
    default=False,
    help='seamless deploy the bundle',
)
def deploy(*args, **kwargs):
    _deploy(*args, **kwargs)
