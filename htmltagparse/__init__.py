"""
A tool designed to quickly parse html tags and elements.
"""
from . import parser
import requests
from .parser import NewPage, html2txt
from . import build

__version__ = "1.0"
__author__ = "xyzpw"
__description__ = "A tool designed to quickly parse html tags and elements."
__license__ = "MIT"

__all__ = [
    "titleFromHtml",
    "titleFromUri",
    "NewPage",
    "build",
]

def titleFromHtml(htmlContent: str) -> str:
    htmlTitle = parser.searchForGroup(r"<title>(?P<title>.*?)</title>", htmlContent, "title")
    return html2txt(htmlTitle)

def titleFromUri(url: str) -> str:
    return titleFromHtml(requests.get(url).text)
