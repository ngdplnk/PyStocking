### INSTALLER BUILD SCRIPT ###

!define ICON_PATH "<TYPE THE ICON.ICO PATH HERE>"
!define LAUNCHER_PATH "<TYPE THE LAUNCHER.PYW PATH HERE>"
!define MAIN_PATH "<TYPE THE MAIN.PYW PATH HERE>"
!define SUBMENUS_PATH "<TYPE THE SUBMENUS FOLDER PATH HERE>"
!define REQUIREMENTS_PATH "<TYPE THE REQUIREMENTS.TXT PATH HERE>"

############################################################

Caption "PyStocking Installer"
UninstallCaption "PyStocking Uninstaller"
!define APP_VERSION "1.0"
!define PRODUCT_VERSION "1.0.0.0"
!define APP_EDITOR "ngdplnk"

Outfile "PyStocking_v1.0_Setup.exe"
SetCompressor /SOLID lzma
Icon "${ICON_PATH}"

SilentInstall silent
SilentUninstall silent

VIProductVersion "${PRODUCT_VERSION}"
VIAddVersionKey "ProductName" "PyStocking"
VIAddVersionKey "CompanyName" "ngdplnk"
VIAddVersionKey "FileDescription" "Manage your inventory with PyStocking"
VIAddVersionKey "FileVersion" "${APP_VERSION}"
VIAddVersionKey "LegalCopyright" "Copyright (C) 2025 ${APP_EDITOR}"
VIAddVersionKey "OriginalFilename" "PyStocking_v1.0_Setup.exe"
VIAddVersionKey "Comments" "Developed by ${APP_EDITOR}"

# Define the installation directory
InstallDir $APPDATA\PyStocking

Section "MainSection" SEC01

  # Set the installer to close automatically when done
  SetAutoClose true

  # Define the directory for the program
  SetOutPath $APPDATA\PyStocking

  # Copy files
  SetOutPath $APPDATA\PyStocking\launcher
  File /oname=launcher.pyw "${LAUNCHER_PATH}"
  
  SetOutPath $APPDATA\PyStocking
  File /oname=main.pyw "${MAIN_PATH}"

  # Copy the submenus folder and its contents
  SetOutPath $APPDATA\PyStocking\submenus
  File /r "${SUBMENUS_PATH}\*.*"

  # Copy icon
  SetOutPath $APPDATA\PyStocking\launcher
  File /oname=icon.ico "${ICON_PATH}"

  # Copy requirements.txt
  SetOutPath $APPDATA\PyStocking
  File /oname=requirements.txt "${REQUIREMENTS_PATH}"

  # Install pip requirements
  ExecWait 'pip install -r "$APPDATA\PyStocking\requirements.txt"'

  # Create a desktop shortcut
  CreateShortCut "$DESKTOP\PyStocking.lnk" "$APPDATA\PyStocking\launcher\launcher.pyw" "" "$APPDATA\PyStocking\launcher\icon.ico" 0

  # Create a Start Menu shortcut
  CreateShortCut "$SMPROGRAMS\PyStocking.lnk" "$APPDATA\PyStocking\launcher\launcher.pyw" "" "$APPDATA\PyStocking\launcher\icon.ico" 0

  # Write the uninstall keys for Add/Remove Programs
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyStocking" "DisplayName" "PyStocking"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyStocking" "UninstallString" "$INSTDIR\uninstaller.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyStocking" "Publisher" "ngdplnk"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyStocking" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyStocking" "DisplayIcon" "$INSTDIR\launcher\icon.ico"
  WriteUninstaller "$INSTDIR\uninstaller.exe"

  # Show a message when the program is completely installed
  MessageBox MB_YESNO|MB_ICONINFORMATION "The program has been installed successfully. Do you want to open it now?" IDYES runProgram

  # Don't run the program if the user clicked "No"
  Goto end

  runProgram:
  # Run the program if the user clicked "Yes"
  ExecShell "" "$APPDATA\PyStocking\launcher\launcher.pyw"

  end:

SectionEnd

Section "Uninstall"

  # Set the uninstaller to close automatically when done
  SetAutoClose true

  # Remove the shortcuts
  Delete "$DESKTOP\PyStocking.lnk"
  Delete "$SMPROGRAMS\PyStocking.lnk"

  # Remove the uninstaller
  Delete "$INSTDIR\uninstaller.exe"

  # Remove the uninstall keys
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\PyStocking"

  # Remove all program files
  RMDir /r $APPDATA\PyStocking

  # Show a message when the program is completely uninstalled
  MessageBox MB_OK|MB_ICONINFORMATION "The program has been uninstalled successfully."

SectionEnd