import re
import htmltagparse
from .html_tags import *
from bs4 import BeautifulSoup
import timeoutcall
from .exceptions import *
import re

__all__ = [
    "NewPage",
    "html2txt",
]

def searchForGroup(pattern: str, text: str, group: str) -> str:
    try:
        return re.search(pattern, text, flags=(re.MULTILINE | re.DOTALL)).group(group)
    except:
        return

def findTags(htmlContent: str) -> list:
    foundTags = []
    for tag in all_tags:
        tagSearch = re.compile(rf"<{tag}\s?(?:.*?)?>(?:.*?)</{tag}>", flags=(re.MULTILINE | re.DOTALL))
        if bool(tagSearch.search(htmlContent)):
            foundTags.append(tag)
    return foundTags

# large pages may hang script
def findSources(htmlContent: str) -> list:
    foundSources = {}
    makeSrcPattern = lambda tag: re.compile(rf'<{tag} [\w\s]*?src="(?P<source>.*?)"(?:.*?)</{tag}>', flags=(re.M|re.S))
    makeVoidSrcPattern = lambda tag: re.compile(rf'<{tag} [\w\s]*?src="(?P<source>.*?)"(?:.*?)/?>', flags=(re.M|re.S))
    for tag in tagsWithSrc:
        srcSearch = re.findall(makeSrcPattern(tag), htmlContent)
        voidSrcSearch = re.findall(makeVoidSrcPattern(tag), htmlContent)
        if bool(srcSearch):
            foundSources[tag] = srcSearch
        if bool(voidSrcSearch) and tag not in foundSources:
            foundSources[tag] = voidSrcSearch
    return foundSources

def findHrefs(htmlContent: str) -> list:
    foundHrefs = {}
    makeHrefPattern = lambda tag: re.compile(rf'<{tag} [\w\s]*?href="(?P<href>.*?)".*?/?>', flags=(re.M|re.S))
    for tag in tagsWithHref:
        hrefSearch = makeHrefPattern(tag).findall(htmlContent)
        aTag = re.findall(r'<a [\w\s]*?href="(?P<href>.*?)">(?:.*?)</a>', htmlContent, flags=(re.M|re.S))
        if bool(hrefSearch):
            foundHrefs[tag] = hrefSearch
        elif bool(aTag):
            foundHrefs[tag] = hrefSearch
    return foundHrefs

def findIds(htmlContent: str) -> list:
    foundIds = []
    idRegexPattern = re.compile(r'<(?:.*?) [\w\s]*?id="(?P<id>.*?)".*?>(?:.*?)</(?:.*?)>', flags=(re.M|re.S))
    voidIdRegexPattern = re.compile(r'<(?:.*?) [\w\s]*?id="(?P<id>.*?)".*?/?>', flags=(re.M|re.S))
    for i in idRegexPattern.findall(htmlContent):
        foundIds.append(i)
    for i in voidIdRegexPattern.findall(htmlContent):
        if i in foundIds:
            continue
        foundIds.append(i)
    return foundIds

def html2txt(htmlContent: str):
    return BeautifulSoup(htmlContent, features="html5lib").get_text()

class NewPage:
    def __init__(self, htmlContent: str, timeout=5):
        makeSrcPattern = lambda tag: re.compile(rf'<{tag} [\w\s]*?src="(?P<source>.*?)"(?:.*?)</{tag}>', flags=(re.M|re.S))
        self.html = htmlContent
        self.text = html2txt(htmlContent)
        self.uri = None
        self.status_code = None
        self.title = htmltagparse.titleFromHtml(htmlContent)
        self.sources = findSources(htmlContent)
        self.hrefs = findHrefs(htmlContent)
        self.ids = findIds(htmlContent)
        try:
            self.tags = timeoutcall.call(findTags, timeout, "", htmlContent)
        except TimeoutError:
            tagError = TagTimeoutException(TagTimeoutException.__doc__)
            if htmlContent == None:
                htmlContent = ''
            tagError.htmlsize = len(htmlContent)
            tagError.timeout = float(timeout)
            self.tags = tagError
    def searchTag(self, tag: str, void=False, htmlFormat=True) -> list:
        """Returns a list of html tag occurrences.

        :param tag:        the tag name to be searched
        :param void:       searches the specified tag as an html void element
        :param htmlFormat: determines whether the target text will be html or text format"""
        if void:
            contents = re.findall(rf'<{tag}\s?(?:.*?)?/?>', self.html, flags=(re.M | re.S))
        else:
            contents = re.findall(rf'<{tag}\s?(?:.*?)?>(?P<txt>.*?)</{tag}>', self.html, flags=(re.M | re.S))
        if not htmlFormat:
            for i in range(len(contents)):
                contents[i] = html2txt(str(contents[i]))
        return contents
    def regex(self, pattern: str, htmlFormat=True, findall=False):
        """Search page content with a regex pattern.
        Regex flags "re.MULTILINE" and "re.DOTALL" are in use with this function.

        :param pattern:    the regex pattern which will be used to search page content
        :param htmlFormat: determines whether the target text will be html or text format
        :param findall:    returns a list of text which matches the specified regex pattern"""
        targetText = str(self.html) if htmlFormat else str(self.text)
        compiledPattern = re.compile(pattern, flags=(re.MULTILINE | re.DOTALL))
        regexMatch = compiledPattern.search(targetText) if not findall else compiledPattern.findall(targetText)
        return regexMatch
