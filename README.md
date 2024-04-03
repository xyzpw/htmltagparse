# htmltagparse
A tool designed to quickly parse html tags and elements.

## Prerequisites
- Pip packages:
  - timeoutcall==1.*
  - beautifulsoup4==4.*
  - html5lib==1.*

## Usage
### Reading Page Titles
Firstly, if you would like to view a page title alone, you could use the `titleFromUri` function:
```python
from htmltagparse import titleFromUri

websiteTitle = titleFromUri("https://github.com/")
print(websiteTitle) # output: GitHub: Let’s build from here · GitHub
```

### Building Pages
#### Building Pages via URI
```python
from htmltagparse import build

brave = build.fromUri("https://search.brave.com/", timeout=20)
print(brave.tags) #list of tags found on the specified page
print(brave.searchTag("footer")) #displays a list of innerHtml content to the footer tags
print(brave.searchTag("footer", htmlFormat=False)[0]) #output: © Brave Software Brave Search API Summarizer Helpful answers Report a security issue
```

#### Building Pages via HTML
```python
from htmltagparse import NewPage
from requests import get

htmlContent = get("https://duckduckgo.com/").text
ddg = NewPage(htmlContent)
print(list(ddg.sources)) #output: script
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

## Developers
### Building To Wheel File
- cd into root directory of this repository
- run `python3 -m build`

> [!NOTE]
> Errors building this package may be due to external package requirements, if this occurs, use `python3 -m build -n` instead.

### Contributions
Must not include:
- Major changes
- Breaking code
- Changes to version number
