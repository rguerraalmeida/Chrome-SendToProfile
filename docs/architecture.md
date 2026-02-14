# Architecture and Security Boundaries

## Overview
The project uses a Chrome MV3 extension plus a Windows native messaging host to open the active tab URL in a different Chrome profile.

1. User clicks extension action.
2. Extension reads active tab URL and user settings.
3. Extension sends JSON message to native host (`chrome.runtime.sendNativeMessage`).
4. Native host validates request and launches Chrome with:
   - `--profile-directory=<Profile Name>`
   - `--new-window`
   - `<URL>`
5. Extension optionally closes source tab if host launch succeeds.

## Why native host is required
Chrome extension APIs do not provide direct control over other profile windows. Native messaging is the supported bridge for privileged local actions.

## Security boundaries
- Extension and native host communicate only through Chrome native messaging.
- Native host manifest allowlists this extension ID.
- Host accepts only strict request schema and supported URL schemes (`http`, `https`).
- Host launches Chrome via argument array (no shell interpolation).

## Non-goals
- No unsupported browser internals or profile data file manipulation.
- No direct profile switching from extension APIs alone.
- No cross-platform support in v1 (Windows only).
