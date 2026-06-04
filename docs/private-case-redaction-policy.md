# Private Case Redaction Policy

Before any case is retained or summarized:

- remove PHI-like fields
- remove raw DICOM files
- remove real hospital names
- remove real vendor confidential rules
- remove real device serial numbers
- remove clinical validation, regulatory approval, and certification upgrade
  language

Partner-facing outputs may include case id, profile version, expected primary
error code, and synthetic/no-PHI flags only.

