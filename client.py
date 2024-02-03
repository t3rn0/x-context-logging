import json

import requests

from context import Context, current_context

url = "http://localhost:8000/root"


def _prepare_context_header():
    return {"X-context": json.dumps(dict(current_context))}


with Context(a=1, b=False):
    requests.get(url, headers=_prepare_context_header())

requests.get(url, headers=_prepare_context_header())
