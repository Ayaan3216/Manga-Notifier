; ─────────────────────────────────────────────────────────────────────────────
;  Manga Notifier v1.5 – Inno Setup Installer Script
;  Replaces any previous MNv1.x installation while preserving user data.
; ─────────────────────────────────────────────────────────────────────────────

#define AppName      "Manga Notifier"
#define AppVersion   "1.5"
#define AppPublisher "Ayaan4uThere"
#define AppURL       "https://github.com/Ayaan3216/Manga-Notifier"
#define AppExeName   "MNv1.5.exe"
#define AppId        "{{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"

[Setup]
AppId={#AppId}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}/issues
AppUpdatesURL={#AppURL}/releases
DefaultDirName={autopf}\MangaNotifier
DefaultGroupName={#AppName}
AllowNoIcons=yes
; Single-file installer — no sub-directory install wizard
OutputDir=dist
OutputBaseFilename=MangaNotifier_v1.5_Setup
SetupIconFile=data\assets\app_icon.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#AppExeName}
; Silently remove old versions that share the same AppId before installing
CloseApplications=yes
RestartIfNeededByRun=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; ── Main executable ──────────────────────────────────────────────────────────
Source: "dist\{#AppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; ── Bundled assets (already embedded in the exe via PyInstaller, but we
;    copy the raw data dir so the data/ folder structure is created on first
;    install — subsequent updates leave the user's tracked.json alone) ────────
; NOTE: The [InstallDelete] section handles removing the OLD exe gracefully.

[Icons]
Name: "{group}\{#AppName}";     Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\{#AppName}";    Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[InstallDelete]
; Remove old executable names so the install dir stays clean.
; User DATA (data\tracked.json, data\prefs.json, data\manga_notifier.log)
; is intentionally NOT listed here — it will be preserved.
Type: files; Name: "{app}\MangaNotifier.exe"
Type: files; Name: "{app}\MNv1.3.exe"
Type: files; Name: "{app}\MNv1.4.exe"

[Code]
{ ──────────────────────────────────────────────────────────────────────────
  Before installation we kill any running instance of the app so that
  the file can be overwritten.  We iterate common process names.
  ────────────────────────────────────────────────────────────────────────── }
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Attempt to close a running Manga Notifier (all known exe names)
  Exec('taskkill.exe', '/F /IM MNv1.4.exe',  '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Exec('taskkill.exe', '/F /IM MNv1.5.exe',  '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Exec('taskkill.exe', '/F /IM MangaNotifier.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := True;
end;
