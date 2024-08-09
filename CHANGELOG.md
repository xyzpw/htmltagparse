# Changelog

## v3.1 (2024-08-09)
- added kwargs to `fromUri` function

## v3 (2024-04-26)
- major changes:
  - renamed `searchTag` to `findall`
  - renamed `getTagContents` to `getInnerHtml`
  - removed `searchTagExists`
  - removed `htmlFormat` from `searchTag`
  - removed `titleFromHtml`

- new functions:
  - fixSpacing: removes additional spaces and optionally newlines
  - fixElementSpacing: fixes the spacing of an html element opening tag
  - find: finds html elements via advanced searching
  - metadataFromUri: retrieves the metadata from an html page via the uri
  - encodeURI: encodes text into a uri format
  - decodeURI: decodes a uri format text into regular text

- enhancements:
  - tag searches are now faster
  - new parsing method which increases speed
  - regex patterns

- changes:
  - module `timeoutcall` is no longer required

- patch:
  - fixed exception's docstrings

## v2.0 (2024-04-09)
- renamed `NewPage` to `HtmlPage`
- timeout GET requests will now raise an exception instead of being returned
- enhanced regex patterns

- new html page instances:
  - encoding
  - lang
  - elapsed
  - metadata

- new html methods:
  - getElementAttributeValue: retrieves a specified attribute value from outerHtml text
  - getElementAttributes: returns a dictionary of attributes and their values from an element's outerHtml text
  - getTagContents: returns the innerHtml of an elements outerHtml

- new html page methods:
  - searchTagExists: verifies a tag with the specified name exists
  - getIdContents: returns the contents of an element assigned to the specified id
