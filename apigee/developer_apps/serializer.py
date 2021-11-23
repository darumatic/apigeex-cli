import json


class AppsSerializer:
    def serialize_details(self, apps, format):
        resp = apps
        if format == 'text':
            return apps.text
        apps = apps.json()
        if format == 'json':
            return json.dumps(apps, indent=2)
        elif format == 'table':
            pass
        elif format == 'dict':
            return apps
        return resp
