"""A tool designed to quickly parse html tags and elements."""

import requests
import requests.utils
from .parser import *
from .build import *
from .cleaner import *
from urllib.parse import quote as encodeURI
from urllib.parse import unquote as decodeURI

__version__ = "3.1"
__author__ = "xyzpw"
__description__ = "A tool designed to quickly parse html tags and elements."
__license__ = "MIT"

__all__ = [
    "titleFromUri",
    "HtmlPage",
    "build",
    "getElementAttributeValue",
    "getElementAttributes",
    "getInnerHtml",
    "fixSpacing",
    "fixElementSpacing",
]

def titleFromUri(url: str, **kwargs) -> str:
    """Retrieves the title of an HTML page linked to a specified URL.

    :param url: the url which points to the html page to be searched

    :kwargs: additional arguments will be passed to the `get` function of the requests module"""
    pageHtml = requests.get(url, **kwargs).text
    pageTitle = parser.titleFromHtml(pageHtml)
    return pageTitle

def metadataFromUri(url: str, **kwargs) -> list[dict]:
    """Returns metadata of an HTML page linked to a specified URL.

    :param url: url to the page that contains the metadata to be returned

    :kwargs: additional arguments will be passed to the `get` function of the requests module"""
    urlContent = requests.get(url, **kwargs).text
    metadata = parser.getHtmlMetadata(urlContent)
    return metadata
