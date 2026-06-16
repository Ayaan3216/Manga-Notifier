# ─────────────────────────────────────────────────────────────────────────────
#  Manga Notifier v1.5 — Updater / Installer
#  Run this script to install or upgrade Manga Notifier.
#  Your tracking data (tracked.json, prefs.json, logs) is always preserved.
# ─────────────────────────────────────────────────────────────────────────────

param(
    [string]$InstallDir = "$env:LOCALAPPDATA\MangaNotifier"
)

$ErrorActionPreference = "Stop"
$AppName    = "Manga Notifier"
$Version    = "v1.6"
$ExeName    = "MNv1.6.exe"
$OldExes    = @("MNv1.5.exe", "MNv1.4.exe", "MNv1.3.exe", "MangaNotifier.exe")
$ShortcutPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop", "$AppName.lnk")
$SourceExe  = Join-Path $PSScriptRoot $ExeName

# ── 0. Check source exists ────────────────────────────────────────────────────
if (-not (Test-Path $SourceExe)) {
    Write-Host "ERROR: $ExeName not found next to this script." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "  ┌─────────────────────────────────────┐" -ForegroundColor Cyan
Write-Host "  │   Manga Notifier Installer  $Version   │" -ForegroundColor Cyan
Write-Host "  └─────────────────────────────────────┘" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Install directory: $InstallDir"
Write-Host ""

# ── 1. Kill any running instances ─────────────────────────────────────────────
foreach ($exe in ($OldExes + $ExeName)) {
    $proc = Get-Process -Name ([System.IO.Path]::GetFileNameWithoutExtension($exe)) -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "  Closing running instance: $exe ..."
        $proc | Stop-Process -Force
        Start-Sleep -Milliseconds 800
    }
}

# ── 2. Create install directory (preserve existing data subfolder) ─────────────
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
$DataDir = Join-Path $InstallDir "data"
New-Item -ItemType Directory -Path $DataDir -Force | Out-Null

# ── 3. Remove OLD executables (keep data untouched) ──────────────────────────
foreach ($old in $OldExes) {
    $oldPath = Join-Path $InstallDir $old
    if (Test-Path $oldPath) {
        Write-Host "  Removing old: $old"
        Remove-Item $oldPath -Force
    }
}

# ── 4. Copy new executable ───────────────────────────────────────────────────
Write-Host "  Installing $ExeName ..."
Copy-Item $SourceExe (Join-Path $InstallDir $ExeName) -Force

# ── 5. Create / update desktop shortcut ──────────────────────────────────────
Write-Host "  Creating desktop shortcut ..."
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath   = Join-Path $InstallDir $ExeName
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.IconLocation = Join-Path $InstallDir $ExeName
$Shortcut.Description  = "Manga Notifier — Chapter tracker"
$Shortcut.Save()

Write-Host ""
Write-Host "  ✅  Manga Notifier $Version installed!" -ForegroundColor Green
Write-Host "  📁  Location : $InstallDir"
Write-Host "  🖥️   Shortcut : Desktop\$AppName"
Write-Host "  📦  Data is preserved in: $DataDir"
Write-Host ""

# ── 6. Launch ─────────────────────────────────────────────────────────────────
$launch = Read-Host "  Launch Manga Notifier now? [Y/n]"
if ($launch -eq "" -or $launch.ToLower() -eq "y") {
    Start-Process (Join-Path $InstallDir $ExeName)
}
