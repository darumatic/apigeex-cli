#!/usr/bin/env python

# Copyright 2019 Matthew Delotavo
# Copyright 2015 Apigee Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import http.client
import io
import json
import logging
import os
import re
import sys
import urllib.parse
import zipfile

from apigee import APIGEE_ADMIN_API_URL, auth, console
from apigee.apis.apis import Apis

url = urllib.parse.urlparse(APIGEE_ADMIN_API_URL)
httpScheme = url[0]
httpHost = url[1]


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def httpCall(verb, uri, headers, body):
    if httpScheme == 'https':
        conn = http.client.HTTPSConnection(httpHost)
    else:
        conn = http.client.HTTPConnection(httpHost)

    if headers == None:
        hdrs = {}
    else:
        hdrs = headers
    hdrs = auth.set_header(Auth, headers=hdrs)
    conn.request(verb, uri, body, hdrs)
    return conn.getresponse()


# Return TRUE if any component of the file path contains a directory name that
# starts with a "." like '.svn', but not '.' or '..'
def pathContainsDot(p):
    c = re.compile('\.\w+')

    for pc in p.split('/'):
        if c.match(pc) != None:
            return True

    return False


def getDeployments():
    # Print info on deployments
    hdrs = {'Accept': 'application/json'}
    resp = httpCall(
        'GET', '/v1/organizations/%s/apis/%s/deployments' % (Organization, Name), hdrs, None
    )

    if resp.status >= 400:
        logging.error(str(resp.readlines()))
        return None
    deployments = json.loads(resp.read().decode()).get("deployments", [])
    return deployments

        
def printDeployments(dep, check_revision=None):
    if check_revision:
        check_revision = str(check_revision)
        revisions = [d['revision'] for d in dep]
        print(revisions, check_revision)
        if check_revision not in revisions:
            sys.exit('Error: proxy version %s not found' % check_revision)
        console.echo('Proxy version %s found' % check_revision)
    for d in dep:
        console.echo('Environment: %s' % d['environment'])
        console.echo('  Revision: %s' % (d['revision']))
        if 'error' in d:
            console.echo('  Error: %s' % d['error'])


def deploy(args):
    global Directory
    global Organization
    global Environment
    global Name
    global ShouldDeploy
    global ShouldOverride
    global Auth
    global ServiceAccount

    Directory = args.directory
    Organization = args.org
    Environment = args.environment
    Name = args.name
    ShouldDeploy = not args.import_only
    ShouldOverride = args.seamless_deploy
    ServiceAccount = args.service_account
    Auth = Struct(
        username=args.username,
        token=args.token
    )

    if Directory != None:
        # Construct a ZIPped copy of the bundle in memory
        tf = io.BytesIO()
        zipout = zipfile.ZipFile(tf, 'w')

        dirList = os.walk(Directory)
        for dirEntry in dirList:
            if not pathContainsDot(dirEntry[0]):
                for fileEntry in dirEntry[2]:
                    if not fileEntry.endswith('~'):
                        fn = os.path.join(dirEntry[0], fileEntry)
                        en = os.path.join(os.path.relpath(dirEntry[0], Directory), fileEntry)
                        console.echo('Writing %s to %s' % (fn, en))
                        zipout.write(fn, en)

        zipout.close()
        body = tf.getvalue()
    #elif ZipFile != None:
    #    f = open(ZipFile, 'r')
    #    body = f.read()
    #    f.close()

    # Upload the bundle to the API
    hdrs = {'Content-Type': 'application/octet-stream', 'Accept': 'application/json'}
    uri = '/v1/organizations/%s/apis?action=import&name=%s' % (Organization, Name)
    resp = httpCall('POST', uri, hdrs, body)

    if resp.status != 200 and resp.status != 201:
        console.echo(
            'Import failed to %s with status %i:\n%s' % (uri, resp.status, resp.read().decode())
        )
        sys.exit(2)

    deployment = json.loads(resp.read().decode())
    revision = int(deployment['revision'])

    console.echo('Imported new proxy version %i' % revision)
    
    if ShouldDeploy and not ShouldOverride:
        # Undeploy duplicates
        deps = getDeployments()
        for d in deps:
            if (
                d['environment'] == Environment
                and d['apiProxy'] == Name
                and d['revision'] != revision
            ):
                console.echo(
                    'Undeploying revision %s in same environment:' % d['revision']
                )
                resp = Apis(Auth, Organization).undeploy_api_proxy_revision(d["apiProxy"], d["environment"], d["revision"])
                if resp.status_code >= 400:
                    console.echo(
                        'Error %i on undeployment:\n%s' % (resp.status_code, resp.text)
                    )

        # Deploy the bundle
        hdrs = {'Accept': 'application/json'}
        resp = Apis(Auth, Organization).deploy_api_proxy_revision(Name, Environment, revision, ServiceAccount)

        if resp.status_code >= 400:
            console.echo('Deploy failed with status %i:\n%s' % (resp.status_code, resp.text))
            sys.exit(2)

    if ShouldOverride:
        # Seamless Deploy the bundle
        console.echo('Seamless deploy %s' % Name)
        hdrs = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = Apis(Auth, Organization).deploy_api_proxy_revision(Name, Environment, revision, ServiceAccount, override=True)
        if resp.status_code >= 400:
            console.echo('Deploy failed with status %i:\n%s' % (resp.status_code, resp.text))
            sys.exit(2)

    deps = getDeployments()
    if ShouldDeploy and not ShouldOverride:
        printDeployments(deps)
    if ShouldOverride:
        printDeployments(deps, check_revision=revision)


def main():
    pass


if __name__ == '__main__':
    main()
