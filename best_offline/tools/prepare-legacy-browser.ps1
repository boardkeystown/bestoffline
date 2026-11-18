# Connected, maintainer-only preparation. Unpacks a portable browser; no installation.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$legacyPath = Join-Path $projectRoot 'build\legacy-firefox'
New-Item -ItemType Directory -Force -Path $legacyPath | Out-Null
Invoke-WebRequest -Uri 'https://archive.mozilla.org/pub/firefox/releases/78.15.0esr/win64/en-US/Firefox%20Setup%2078.15.0esr.exe' -OutFile (Join-Path $legacyPath 'firefox-setup.exe')
Invoke-WebRequest -Uri 'https://www.7-zip.org/a/7zr.exe' -OutFile (Join-Path $legacyPath '7zr.exe')
Invoke-WebRequest -Uri 'https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-win64.zip' -OutFile (Join-Path $legacyPath 'geckodriver.zip')
& (Join-Path $legacyPath '7zr.exe') x (Join-Path $legacyPath 'firefox-setup.exe') ("-o" + (Join-Path $legacyPath 'firefox78')) -y
if ($LASTEXITCODE -ne 0) { throw 'Firefox extraction failed' }
Expand-Archive -LiteralPath (Join-Path $legacyPath 'geckodriver.zip') -DestinationPath (Join-Path $legacyPath 'driver') -Force
