# Partner Review Protocol v0.4

This protocol supports synthetic partner review of UDI-DICOM evidence manifest
behavior. It does not share private-only cases unless a separate internal review
process explicitly approves that access.

Before NDA:

- share partner-safe summary documents only
- share synthetic partner pack manifests only
- do not share private cases
- do not share real vendor-confidential rules
- do not accept PHI or raw DICOM files

After NDA:

- review partner-specific questions using synthetic fixtures first
- document any requested mapping separately from real vendor-confidential rules
- keep private regression evidence internal unless explicitly approved

Boundary:

- synthetic-only
- no PHI
- not clinical validation
- not regulatory approval
- not certification
