# Changelog

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