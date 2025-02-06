import os
import sys
import json
import requests
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon

if sys.platform == 'win32':
    PROGRAM_PATH = os.path.join(os.environ.get("APPDATA"), "PyStocking")
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser("~"), ".pystocking")
LAUNCHER_PATH = os.path.join(PROGRAM_PATH, "launcher")
INFO_PATH = os.path.join(PROGRAM_PATH, "info.json")
ICON_PATH = os.path.join(LAUNCHER_PATH, "icon.ico")
UPDATER_ICON_PATH = os.path.join(LAUNCHER_PATH, "upd_icon.ico")
LAUNCHERSCRIPT_PATH = os.path.join(LAUNCHER_PATH, "launcher.pyw")
MAIN_PATH = os.path.join(PROGRAM_PATH, "main.pyw")
SUBMENUS_PATH = os.path.join(PROGRAM_PATH, "submenus")
ADDITEMS_PATH = os.path.join(SUBMENUS_PATH, "add_items")
ADDITEMS_MENU_PATH = os.path.join(ADDITEMS_PATH, "menu.py")
ADVOPTIONS_PATH = os.path.join(SUBMENUS_PATH, "advanced_options")
ADVOPTIONS_MENU_PATH = os.path.join(ADVOPTIONS_PATH, "menu.py")
MANAGEITEMS_PATH = os.path.join(SUBMENUS_PATH, "manage_items")
MANAGEITEMS_MENU_PATH = os.path.join(MANAGEITEMS_PATH, "menu.py")

os.makedirs(PROGRAM_PATH, exist_ok=True)
os.makedirs(LAUNCHER_PATH, exist_ok=True)
os.makedirs(SUBMENUS_PATH, exist_ok=True)
os.makedirs(ADDITEMS_PATH, exist_ok=True)
os.makedirs(ADVOPTIONS_PATH, exist_ok=True)
os.makedirs(MANAGEITEMS_PATH, exist_ok=True)

try:
    session = requests.Session()

    # Check versionCode
    link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/info.json"
    code = session.get(link)
    remote_version = code.json()
    local_version = None
    if os.path.isfile(INFO_PATH):
        with open(INFO_PATH, "r") as file:
            local_version = json.load(file)
    if local_version is None or local_version["versionCode"] < remote_version["versionCode"]:
        # Icon
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/launcher/icon.ico"
        code = session.get(link)
        with open(ICON_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Updater Icon
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/launcher/upd_icon.ico"
        code = session.get(link)
        with open(UPDATER_ICON_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Launcher Script
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/launcher/launcher.pyw"
        code = session.get(link)
        with open(LAUNCHERSCRIPT_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Add Items Menu
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/submenus/add_items/menu.py"
        code = session.get(link)
        with open(ADDITEMS_MENU_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Advanced Options Menu
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/submenus/advanced_options/menu.py"
        code = session.get(link)
        with open(ADVOPTIONS_MENU_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Manage Items Menu
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/submenus/manage_items/menu.py"
        code = session.get(link)
        with open(MANAGEITEMS_MENU_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Main Program
        link = "https://raw.githubusercontent.com/ngdplnk/PyStocking/main/main.pyw"
        code = session.get(link)
        with open(MAIN_PATH, 'wb') as writecode:
            writecode.write(code.content)
        # Info
        with open(INFO_PATH, "w") as file:
            json.dump(remote_version, file)
        # Run the program
        if sys.platform == 'win32':
            subprocess.Popen(f"python {MAIN_PATH}", creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.system(f"python3 {MAIN_PATH}")
    else:
        # Run the program
        if sys.platform == 'win32':
            subprocess.Popen(f"python {MAIN_PATH}", creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.system(f"python3 {MAIN_PATH}")  
except Exception:
    if os.path.isfile(MAIN_PATH) and os.path.isfile(ADDITEMS_MENU_PATH) and os.path.isfile(ADVOPTIONS_MENU_PATH) and os.path.isfile(MANAGEITEMS_MENU_PATH):
        if sys.platform == 'win32':
            subprocess.Popen(f"python {MAIN_PATH}", creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.system(f"python3 {MAIN_PATH}")
    else:
        app = QApplication(sys.argv)
        if os.path.exists(ICON_PATH):
            app.setWindowIcon(QIcon(ICON_PATH))
        QMessageBox.critical(None, "Error", "The program could not be started. Please check your internet connection and try again.")
        sys.exit(1)
