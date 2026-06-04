# Partner Question Bank v0.5

| Question | Safe Technical Answer |
| --- | --- |
| Why require de-identified or synthetic samples? | The suite is designed to keep technical manifest review separate from PHI handling and clinical operations. |
| Is the public validator certification? | No. It is a deterministic consistency checker and not certification, clinical validation, or regulatory approval. |
| What is the partner pack? | A partner-safe summary surface that excludes complete private case content. |
| What is the private suite? | An internal synthetic regression and conformance resource with private cases retained inside this repository. |
| Why use registry fixtures? | Offline fixtures keep review deterministic; live lookup is a separate explicit choice. |
| What is the minimal UDI-DICOM evidence loop? | Manifest, synthetic metadata fixture, registry fixture, evidence item hash, receipt, and report. |
| What is FDO-style mapping? | Optional metadata alignment language, not an official FDO implementation or persistent identifier service. |

## v0.6 Additions

| Question | Safe Technical Answer |
| --- | --- |
| Can we submit real samples through partner feedback? | No. Real cooperation requires NDA and de-identification gates before technical work. |
| Can private cases be cited in a public paper? | No. Only the existence of controlled partner-review infrastructure may be mentioned publicly. |
| Can feedback request certification wording? | No. Certification, regulatory approval, and clinical validation requests are out of scope. |
