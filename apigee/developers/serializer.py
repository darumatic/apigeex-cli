import json


class DevelopersSerializer:
    def serialize_details(self, developers, format):
        resp = developers
        if format == 'text':
            return developers.text
        developers = developers.json()
        if format == 'json':
            return json.dumps(developers, indent=1)
        elif format == 'table':
            pass
        elif format == 'dict':
            return developers
        return resp
