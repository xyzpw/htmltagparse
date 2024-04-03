from .parser import NewPage
import requests
import time
from .exceptions import *

__all__ = [
    "fromUri",
]

def fromUri(uri: str, timeout=5, headers={}) -> object:
    priorEpoch = time.time()
    try:
        resp = requests.get(uri, timeout=timeout, headers=headers)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        htmlError = RequestTimeoutException(RequestTimeoutException.__doc__)
        htmlError.uri = str(uri)
        htmlError.timeout = float(timeout)
        return htmlError
    tagTimeout = timeout - (time.time() - priorEpoch)
    pageHtml = resp.text
    page = NewPage(pageHtml, timeout=tagTimeout)
    page.uri = resp.url
    page.status_code = resp.status_code
    return page
