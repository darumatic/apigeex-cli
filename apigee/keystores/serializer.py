import json


class KeystoresSerializer:
    def serialize_details(self, keystores, format):
        resp = keystores
        if format == 'text':
            return keystores.text
        keystores = keystores.json()
        if format == 'json':
            return json.dumps(keystores, indent=2)
        elif format == 'table':
            pass
        elif format == 'dict':
            return keystores
        return resp
