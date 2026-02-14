param(
  [Parameter(Mandatory=$true)] [string]$ExtensionId,
  [Parameter(Mandatory=$true)] [string]$HostScriptPath
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $HostScriptPath)) {
  throw "Host script path not found: $HostScriptPath"
}

$manifestTemplate = Join-Path $PSScriptRoot "native-host-manifest.template.json"
$launcherTemplate = Join-Path $PSScriptRoot "host-launcher.template.cmd"
$installDir = Join-Path $env:LOCALAPPDATA "SendToProfile"
$manifestPath = Join-Path $installDir "com.send_to_profile.host.json"
$launcherPath = Join-Path $installDir "host-launcher.cmd"

New-Item -ItemType Directory -Path $installDir -Force | Out-Null

if (-not (Test-Path $launcherTemplate)) {
  throw "Launcher template not found: $launcherTemplate"
}

$hostScriptForCmd = $HostScriptPath.Replace('"', '""')
(Get-Content $launcherTemplate -Raw).
  Replace('__HOST_SCRIPT_PATH__', $hostScriptForCmd) | Set-Content $launcherPath -Encoding ASCII

$launcherPathEscaped = $launcherPath.Replace('\\', '\\\\')
(Get-Content $manifestTemplate -Raw).
  Replace('__HOST_PATH__', $launcherPathEscaped).
  Replace('__EXTENSION_ID__', $ExtensionId) | Set-Content $manifestPath -Encoding UTF8

$registryPath = "HKCU:\Software\Google\Chrome\NativeMessagingHosts\com.send_to_profile.host"
New-Item -Path $registryPath -Force | Out-Null
Set-ItemProperty -Path $registryPath -Name "(default)" -Value $manifestPath

Write-Host "Installed launcher: $launcherPath"
Write-Host "Installed native host manifest: $manifestPath"
Write-Host "Registered key: $registryPath"
