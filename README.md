# Chrome-SendToProfile

Chrome extension and Windows native host prototype to send the active tab URL to another Chrome profile.

## Current status
- Ordered issue drafts are available in `docs/issues/`.
- MVP implementation includes:
  - MV3 extension scaffold (`extension/`)
  - Native messaging protocol docs (`docs/protocol.md`)
  - Windows native host prototype (`native-host/windows/src/host.py`)
  - Windows host installer scripts (`native-host/windows/install/`)

## Quick start
1. Load unpacked extension from `extension/`.
2. Install native host using instructions in `docs/setup-windows.md`.
3. Configure profile in extension options and click extension action on an `http/https` tab.

## Repository layout
- `extension/`: Chrome extension (MV3).
- `native-host/windows/`: Windows native host and installation scripts.
- `docs/`: architecture, protocol, setup, release checklist, issue drafts.

## PR creation troubleshooting
If you get errors when creating a pull request, run preflight checks:

```bash
./scripts/pr-preflight.sh
```

See detailed fixes in `docs/troubleshooting-pr.md`.
