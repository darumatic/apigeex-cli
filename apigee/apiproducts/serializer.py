import json


class ApiproductsSerializer:
    def serialize_details(self, apiproducts, format):
        resp = apiproducts
        if format == 'text':
            return apiproducts.text
        apiproducts = apiproducts.json()
        if format == 'json':
            return json.dumps(apiproducts, indent=1)
        elif format == 'table':
            pass
        elif format == 'dict':
            return apiproducts
        return resp
