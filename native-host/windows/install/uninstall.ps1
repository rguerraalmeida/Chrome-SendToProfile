$ErrorActionPreference = "Stop"

$registryPath = "HKCU:\Software\Google\Chrome\NativeMessagingHosts\com.send_to_profile.host"
if (Test-Path $registryPath) {
  Remove-Item -Path $registryPath -Force
  Write-Host "Removed registry key: $registryPath"
} else {
  Write-Host "Registry key not found: $registryPath"
}

$installDir = Join-Path $env:LOCALAPPDATA "SendToProfile"
if (Test-Path $installDir) {
  Remove-Item -Path $installDir -Recurse -Force
  Write-Host "Removed install dir: $installDir"
}
