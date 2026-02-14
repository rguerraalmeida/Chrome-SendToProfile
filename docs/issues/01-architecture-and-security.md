# Architecture and Security Boundaries for Send-To-Profile

## Goal
Document supported architecture and security boundaries for MV3 extension + Windows native host.

## Tasks
- Describe extension, native host, native host manifest, and installer roles.
- Document data flow from active tab URL to launched Chrome window in target profile.
- Explicitly document non-goals and API constraints.
- Add threat model summary and required mitigations.

## Acceptance Criteria
- `docs/architecture.md` exists.
- Includes allowed vs disallowed approaches and why.
- Includes security controls checklist.
