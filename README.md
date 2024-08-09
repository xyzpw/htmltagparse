# htmltagparse
![Pepy Total Downlods](https://img.shields.io/pepy/dt/htmltagparse)

A tool designed to quickly parse HTML tags and elements.

## Prerequisites
- Pip packages:
  - beautifulsoup4==4.*
  - html5lib==1.*
  - requests==2.*

- Optional packages:
  - timeoutcall==1.*

## Usage
### Reading Page Titles
Firstly, if you would like to view page info alone, you could use a few functions for this:
```python
import htmltagparse
title = htmltagparse.titleFromUri("https://github.com/")
print(title) # output: GitHub: Let’s build from here · GitHub

metadata = htmltagparse.metadataFromUri("https://github.com/") # meta tags from github
```

### Building Pages
#### Building Pages via URI
```python
from htmltagparse import build

brave = build.fromUri("https://search.brave.com/")
print(brave.response) #output: (200, 'OK')
print(brave.tags) #list of tags found on the specified page
print(brave.elapsed) #the time taken to create the html page class
print(brave.title) #title of the html page
```
This is not limited to these values alone; there are more values associated with an html page.

#### Building Pages via HTML
```python
from htmltagparse import HtmlPage
from requests import get

htmlContent = get("https://duckduckgo.com/").text
ddg = HtmlPage(htmlContent)
print(list(ddg.sources)) #output: ['script']
```

#### Searching A Page
With this package, you have the ability to search the html page you have created directly through a function:
```python
from htmltagparse import build
import re

videoId = ""
page = build.fromUri("https://www.youtube.com/watch?v=%s" % videoId)
try:
  #NOTE: the regex function already has re's MULTILINE and DOTALL flags in use
  #get a list of tags to the youtube video via this regex pattern
  videoTags = page.regex(r"\"keywords\":(?P<tags>\[.*?),\"channelId\":").group("tags")
  #converting from string to array
  videoTags = re.findall(r"(?:\"|\')(?P<tag>.*?)(?:\'|\")(?:\,|\])", videoTags)
except:
  videoTags = "no tags found"

print(videoTags)
```

Another way you could get tags from a Youtube video is with the `find` function, example:
```python
import htmltagparse

videoId = "" #video id here
yt = htmltagparse.build.fromUri("https://www.youtube.com/watch?v=%s" % videoId)
elTagOpening = yt.find("meta", attrs={"name": "keywords"})[0]
videoKeywords = htmltagparse.getElementAttributeValue(elTagOpening, "content").split(", ")
print(videoKeywords) # tags of the youtube video
```

## Developers
### Building to Wheel File
- cd into root directory of this repository
- run `python3 -m build`

> [!NOTE]
> Errors building this package may be due to this packages requirements, if this occurs, use `python3 -m build -n` instead.

### Contributions
Must not include:
- Major changes
- Breaking code
- Changes to version number
