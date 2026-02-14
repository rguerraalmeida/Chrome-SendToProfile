# Windows Setup (Win10/Win11)

## 1) Load extension (developer mode)
1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select `extension/`.
4. Open extension options and set target profile (e.g. `Profile 1`).

## 2) Install native host
1. Keep `native-host/windows/src/host.py` in a stable location.
2. Open PowerShell in `native-host/windows/install`.
3. Run:
   - `./install.ps1 -ExtensionId <your_extension_id> -HostScriptPath <absolute_path_to_host.py>`
4. The installer writes a launcher at `%LOCALAPPDATA%\SendToProfile\host-launcher.cmd` and registers the native host manifest in HKCU.

## 3) Validate
- Click extension action on an `https://` page.
- Confirm a new Chrome window opens in target profile.

## Troubleshooting
- Host not found: re-run install script, verify registry key exists at `HKCU\Software\Google\Chrome\NativeMessagingHosts\com.send_to_profile.host`.
- Invalid profile: check options value exactly matches Chrome profile directory.
- Launch failure: verify Python launcher (`py` or `python`) is available in PATH.
