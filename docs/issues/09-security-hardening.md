# Security Hardening for Host and Extension

## Goal
Harden parsing/validation and prevent command injection.

## Tasks
- Enforce URL scheme and size limits.
- Reject unknown/invalid payload shapes.
- Use subprocess arg arrays, never shell strings.
- Add negative tests.

## Acceptance Criteria
- Hardened checks implemented and tested.
- Security section updated in docs.
