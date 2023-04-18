import json


def parse_json(json_str: str, required_fields=None,
               keywords=None, keyword_callback=None):

    if keyword_callback is None:
        raise TypeError('no handler')

    json_doc = json.loads(json_str)

    if required_fields is None:
        required_fields = json_doc.keys()

    for field in required_fields:
        if field in json_doc:
            val = json_doc[field].split()
            if keywords is None:
                keywords = val
            req = filter(lambda x: x in keywords, val)
            for req_val in req:
                keyword_callback(field, req_val)
