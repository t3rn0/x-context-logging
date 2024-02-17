import json
import threading

import requests

from context import Context, current_context

BASE_URL = "http://localhost:8000/root"


def _prepare_context_header():
    return {"X-context": json.dumps(dict(current_context))}


def request(url, **kwargs):
    with Context(**kwargs):
        requests.get(url, headers=_prepare_context_header())


def main():
    threads = [
        threading.Thread(
            target=request,
            args=(f"{BASE_URL}/sync",),
            kwargs={"sync_method": True, "some_var": 1},
        ),
        threading.Thread(
            target=request,
            args=(f"{BASE_URL}/sync",),
            kwargs={"sync_method": True, "some_var": 2},
        ),
        threading.Thread(
            target=request,
            args=(f"{BASE_URL}/async",),
            kwargs={"sync_method": False, "some_var": 3},
        ),
        threading.Thread(
            target=request,
            args=(f"{BASE_URL}/async",),
            kwargs={"sync_method": False, "some_var": 4},
        ),
    ]

    for t in threads:
        t.start()


if __name__ == "__main__":
    main()
