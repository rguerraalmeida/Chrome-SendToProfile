# Scaffold MV3 Extension

## Goal
Create an MV3 extension base that captures current tab URL and is ready to send native messages.

## Tasks
- Add `manifest.json` with required permissions.
- Add background service worker.
- Add options page for profile + close tab settings.
- Add storage defaults.

## Acceptance Criteria
- Extension loads as unpacked extension.
- Action click can read current tab URL.
- Options are persisted in `chrome.storage.sync`.
