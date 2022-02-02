import json


class ReferencesSerializer:
    def serialize_details(self, references, format):
        resp = references
        if format == 'text':
            return references.text
        references = references.json()
        if format == 'json':
            return json.dumps(references)
        elif format == 'table':
            pass
        elif format == 'dict':
            return references
        return resp
