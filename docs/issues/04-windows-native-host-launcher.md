# Implement Windows Native Host Launcher

## Goal
Implement native messaging host to validate input and launch Chrome with target profile/new window.

## Tasks
- Read/write native messaging framed JSON.
- Validate action/profile/url.
- Safely launch Chrome with args array.
- Return structured response with request id.

## Acceptance Criteria
- Local protocol tests pass.
- Host returns clear errors for invalid input.
