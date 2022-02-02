import json

from tabulate import tabulate


class DeploymentsSerializer:
    def serialize_details(self, deployment_details, format, showindex=False, tablefmt='plain'):
        if format == 'text':
            return deployment_details.text
        revisions = []
        for i in deployment_details.json()['deployments']:
            revisions.append(
                {
                    'apiProxy': i['apiProxy'],
                    'revision': i['revision'],
                    'environment': i['environment'],
                }
            )
        if format == 'json':
            return json.dumps(revisions, indent=2)
        elif format == 'table':
            table = [[rev['apiProxy'], rev['revision'], rev['environment']] for rev in revisions]
            headers = []
            if showindex == 'always' or showindex is True:
                headers = ['id', 'apiProxy', 'revision', 'environment']
            elif showindex == 'never' or showindex is False:
                headers = ['apiProxy', 'revision', 'environment']
            return tabulate(table, headers, showindex=showindex, tablefmt=tablefmt)
        else:
            raise ValueError(format)
