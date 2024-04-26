import re
from .exceptions import *
from .html_tags import *
from . import parser

__all__ = [
    "fixSpacing",
    "fixElementSpacing",
]

def fixSpacing(stringContent: str, remove_newlines: bool = False) -> str:
    """Removes multiple spaces between words.

    :param stringContent:   the string which will be returned without unwanted spaces
    :param remove_newlines: removes newlines from the fixed string"""
    fixedString = re.sub(r"(?:\s{2,})", " ", stringContent)
    return fixedString.replace("\n", "") if remove_newlines else fixedString

def fixElementSpacing(tagOpeningContent: str) -> str:
    """Removes additional spaces within an HTML element's opening tag

    :param tagOpeningContent: the html element's opening tag which needs to be fixed"""
    tagName = parser.searchForGroup(r"<\s*(?P<tag>\w{1,})", tagOpeningContent, "tag")
    openingTagAttributes = parser.getElementAttributes(tagOpeningContent)
    containsClosingSlash = re.search(rf"<\s*{tagName}.*?/\s*>", tagOpeningContent) != None
    completeWorkingElement = lambda: workingElement + "/>" if containsClosingSlash else workingElement + ">"

    workingElement = "<%s" % tagName
    if openingTagAttributes == None:
        return completeWorkingElement()
    for attr, value in openingTagAttributes.items():
        try:
            quote = re.search(rf"<\s*{tagName}.*?{attr}\s*=\s*(?P<q>\"|\')", tagOpeningContent).group("q")
        except AttributeError:
            quote = '"' # Something went wrong...
        workingElement += " %s=%s%s%s" % (attr, quote, value, quote)
    return completeWorkingElement()
