import json


class CachesSerializer:
    def serialize_details(self, caches, format):
        resp = caches
        if format == 'text':
            return caches.text
        caches = caches.json()
        if format == 'json':
            return json.dumps(caches, indent=2)
        elif format == 'table':
            pass
        elif format == 'dict':
            return caches
        return resp
