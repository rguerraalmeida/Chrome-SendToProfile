# Wire Extension to Native Host

## Goal
Send URL/profile request from extension to native host and show status.

## Tasks
- Implement `sendNativeMessage` in service worker.
- Handle host unavailable and launch errors.
- Show clear success/failure notifications.

## Acceptance Criteria
- Extension receives and handles host response.
- User sees actionable feedback.
