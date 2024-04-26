import re
from .html_tags import *
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning, XMLParsedAsHTMLWarning
try:
    import timeoutcall
    # htmltagparse.parser.hasTimeoutcall can be set to False to avoid using it
    if tuple(timeoutcall.__version__.split("."))[0] == "1":
        hasTimeoutcall = True
except:
    hasTimeoutcall = False
from .exceptions import *
import re
import warnings

__all__ = [
    "HtmlPage",
    "html2txt",
    "getElementAttributes",
    "getElementAttributeValue",
    "getInnerHtml",
]

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

def searchForGroup(pattern: str, text: str, group: str, case_sensitive=True) -> str:
    try:
        flags = re.MULTILINE | re.DOTALL if case_sensitive else re.MULTILINE | re.DOTALL | re.IGNORECASE
        return re.search(pattern, text, flags=flags).group(group)
    except:
        return

def findTags(htmlContent: str) -> list:
    foundTags = []
    for tag in all_tags:
        tagSearch = re.search(rf"<\s*{tag}.*?>", htmlContent, re.MULTILINE | re.DOTALL)
        if not tag in voidTags and tagSearch != None:
            tagSearchMatch = tagSearch.group(0)
            tagSearchSpan = tagSearch.span()
            strippedHtmlContent = htmlContent[tagSearchSpan[0]:]
            tagContentSearch = re.search(rf"{re.escape(tagSearchMatch)}.*?<\s*/\s*{tag}\s*>",
                strippedHtmlContent,
                flags=(re.MULTILINE | re.DOTALL),
            )
            if tagContentSearch != None:
                foundTags.append(tag)
        elif tag in voidTags and tagSearch != None:
            foundTags.append(tag)
    return foundTags

def findSources(htmlContent: str) -> list:
    foundSources = {}
    for tag in tagsWithSrc:
        srcIter = re.finditer(
            rf"<\s*{tag}[^>]*?src\s*=\s*(\"|\')(?P<src>.*?)(?:\1).*?>",
            htmlContent,
            flags=(re.MULTILINE | re.DOTALL),
        )
        sources = []
        for src in srcIter:
            currentSrc = src.group("src")
            if currentSrc != None:
                sources.append(currentSrc)
        if sources != []:
            foundSources[tag] = sources
    return foundSources

def findHrefs(htmlContent: str) -> list:
    foundHrefs = {}
    for tag in tagsWithHref:
        hrefIter = re.finditer(
            rf"<\s*{tag}[^>]*?href\s*=\s*(\"|\')(?P<href>.*?)(?:\1).*?>",
            htmlContent,
            flags=(re.MULTILINE | re.DOTALL),
        )
        hrefs = []
        for href in hrefIter:
            currentHref = href.group("href")
            if currentHref != None:
                hrefs.append(currentHref)
        if hrefs != []:
            foundHrefs[tag] = hrefs
    return foundHrefs

def findIds(htmlContent: str) -> list:
    foundIds = []
    for tag in all_tags:
        idIter = re.finditer(
            rf"<\s*{tag}[^>]*?id\s*=\s*(\"|\')(?P<id>.*?)(?:\1).*?>",
            htmlContent,
            flags=(re.MULTILINE | re.DOTALL),
        )
        for i in idIter:
            currentId = i.group("id")
            if currentId != None:
                foundIds.append(currentId)
    return list(set(foundIds))

def getElementAttributeValue(elementOpeningTag: str, attrName: str) -> str:
    """Returns the value of an HTML attribute value.

    :param elementOpeningTag: the element opening tag which contains the attribute to be searched
    :param attrName:          the attribute name which contains the value to be returned"""
    elementOpeningTag = elementOpeningTag[elementOpeningTag.index("<"):]
    tagName = searchForGroup(r"<\s*(?P<tag>[\w\-]{1,})", elementOpeningTag, "tag")
    attrValue = searchForGroup(
        rf"<\s*{tagName} (?:[^>]*?){attrName}\s*=\s*(\"|\')(?P<value>.*?)(?:\1).*?>",
        elementOpeningTag,
        "value"
    )
    return attrValue

def getElementAttributes(elementOpeningTag: str) -> dict[str, str]:
    """Returns a dictionary of attributes associated with an HTML element.

    :param elementOpeningTag: the element opening tag of which contains attributes to be returned"""
    elementOpeningTag = elementOpeningTag[elementOpeningTag.index("<"):]
    tagName = searchForGroup(r"^<\s*(?P<tag>[\w\-]{1,})", elementOpeningTag, "tag")
    tagOpening = searchForGroup(rf"<\s*{tagName} (?P<opening>.*?)\s*/?\s*>", elementOpeningTag, "opening")
    if tagOpening == None:
        return
    attributeIter = re.finditer(r"(?P<attr>[\w\-]{1,})\s*=\s*(\"|\')(?P<value>.*?)(?:\2)", tagOpening)
    attributes = {}
    for attrIter in attributeIter:
        attributes[attrIter.group("attr")] = attrIter.group("value")
    return attributes

def getInnerHtml(outerHtml: str) -> str:
    """Returns the inner HTML of an element via outer HTML.

    :param outerHtml: the outer html contents which contain the inner html to be returned"""
    outerHtml = outerHtml[outerHtml.index("<"):]
    tagName = searchForGroup(r"<\s*(?P<tag>\w{1,})", outerHtml, "tag")
    innerHtml = searchForGroup(
        rf"<\s*{tagName}.*?>(?P<content>.*?)<\s*/\s*{tagName}\s*>",
        outerHtml,
        "content"
    )
    return innerHtml

def getHtmlMetadata(htmlContent: str) -> list[dict]:
    metadataContents = []
    metaTags = re.findall(r"<\s*meta (?:.*?)>", htmlContent, re.MULTILINE | re.DOTALL)
    for i in range(len(metaTags)):
        metaTags[i] = re.sub(r"<\s*meta (?P<cont>.*?)\s*/?\s*>", r"\g<cont>", metaTags[i])
    for tag in metaTags:
        workingMetadataDict = {}
        workingMetadataIter = re.finditer(r"(?P<attr>[\w\-]{1,})\s*=\s*(\"|\')(?P<value>.*?)(?:\2)", tag)
        for currIter in workingMetadataIter:
            workingMetadataDict[currIter.group("attr")] = currIter.group("value")
        metadataContents.append(workingMetadataDict)
    return metadataContents

def titleFromHtml(htmlContent: str) -> str:
    pageTitle = searchForGroup(r"<\s*title\s*>(?P<title>.*?)<\s*/\s*title\s*>", htmlContent, "title")
    return html2txt(pageTitle)

def html2txt(htmlContent: str):
    """Parses HTML data into plain text."""
    return BeautifulSoup(str(htmlContent), features="html5lib").get_text()

class HtmlPage:
    """Contains information from HTML text."""
    def __init__(self, htmlContent: str, timeout=5):
        self.html = htmlContent if htmlContent != None else ''
        self.text = html2txt(htmlContent)
        self.uri = None
        self.response = None
        self.title = titleFromHtml(self.html)
        self.sources = findSources(htmlContent)
        self.hrefs = findHrefs(htmlContent)
        self.ids = findIds(htmlContent)
        self.lang = searchForGroup(r"<\s*html.*?lang\s*=\s*(\"|\')(?P<lang>.*?)(?:\1).*?>", self.html, "lang", False)
        self.encoding = searchForGroup(r"<\s*meta.*?charset\s*=\s*(\"|\')(?P<encoding>.*?)(?:\1).*?>", self.html, "encoding", False)
        self.metadata = getHtmlMetadata(self.html)
        if hasTimeoutcall:
            try:
                self.tags = timeoutcall.call(findTags, timeout, "could not fetch tags within timeout duration", htmlContent)
            except TimeoutError as ERROR:
                self.tags = HtmlTagError(str(ERROR))
        else:
            self.tags = findTags(self.html)
    def __str__(self):
        return self.uri
    def __repr__(self):
        return repr(list(vars(self)))
    def findall(self, tagName: str) -> list:
        """Returns a list of HTML tag occurrences.

        :param tag: the tag name to be searched"""
        contents = []
        if tagName in voidTags:
            tagsFound = re.findall(rf"<\s*{tagName}.*?>", self.html, flags=(re.MULTILINE | re.DOTALL))
            for tag in tagsFound:
                contents.append(tag)
        else:
            tagIterSearch = re.finditer(rf"<\s*{re.escape(tagName)}.*?>", self.html, re.MULTILINE | re.DOTALL)
            tagIters = [i for i in tagIterSearch]
            del tagIterSearch
            for i in tagIters:
                tagAppearancePos = i.span()[0]
                workingHtmlContent = self.html[tagAppearancePos:]
                tagSearch = re.search(
                    rf"{re.escape(i.group(0))}(?:.*?)<\s*/\s*{tagName}\s*>",
                    workingHtmlContent,
                    flags=(re.MULTILINE | re.DOTALL),
                )
                if bool(tagSearch):
                    contents.append(tagSearch.group(0))
        return contents
    def regex(self, pattern: str, findall=False, htmlFormat=True):
        """Search page content with a regex pattern.
        Regex flags "re.MULTILINE" and "re.DOTALL" are in use with this function.

        :param pattern:    the regex pattern which will be used to search page content
        :param findall:    returns a list of text which matches the specified regex pattern
        :param htmlFormat: determines whether the target text will be html or text format"""
        targetText = str(self.html) if htmlFormat else str(self.text)
        compiledPattern = re.compile(pattern, flags=(re.MULTILINE | re.DOTALL))
        regexMatch = compiledPattern.search(targetText) if not findall else compiledPattern.findall(targetText)
        return regexMatch
    def getIdContents(self, elementId: str, htmlFormat=True) -> str:
        """Returns the innerHtml contents of an element with a specified ID.

        :param elementId:  the id of which is assigned to the element that contains the contents to be returned
        :param htmlFormat: determines whether the contents will be returned in html or text format"""
        for tag in nonVoidTags:
            idContent = searchForGroup(
                rf"<\s*{tag}.*?id\s*=\s*(\"|\')(?:{elementId})(?:\1).*?>(?P<content>.*?)<\s*/\s*{tag}\s*>",
                self.html,
                "content",
            )
            if idContent != None:
                if not htmlFormat:
                    idContent = html2txt(idContent)
                return idContent
    def find(self, tagName: str, attrs: dict) -> list[dict]:
        """Searches for an element with specified attributes.

        :param tagName: tag name of element that needs to be searched
        :param attrs:   attributes and their values within the opening element"""
        if len(list(attrs)) < 1:
            raise HtmlTagError("this function requires at least one attribute value")
        elements = self.findall(tagName)
        matchedElements = []
        for el in elements:
            isInvalid = False
            attributesWithinElement = getElementAttributes(el)
            if attributesWithinElement == None:
                continue
            for attribute in attrs:
                if attribute not in list(attributesWithinElement):
                    isInvalid = True
                    break
            if isInvalid:
                continue
            for elementAttr, elementAttrValue in attributesWithinElement.items():
                if elementAttr in list(attrs):
                    if attrs.get(elementAttr) != elementAttrValue:
                        isInvalid = True
                        continue
            if not isInvalid:
                matchedElements.append(el)
        if matchedElements != []:
            return matchedElements
