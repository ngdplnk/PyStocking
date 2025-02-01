import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox

if sys.platform == 'win32':
    PROGRAM_PATH = os.path.join(os.environ.get("APPDATA"), "PyStocking")
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser("~"), ".pystocking")
LAUNCHER_PATH = os.path.join(PROGRAM_PATH, "launcher")
ICON_PATH = os.path.join(LAUNCHER_PATH, "icon.ico")
LAUNCHERSCRIPT_PATH = os.path.join(LAUNCHER_PATH, "launcher.pyw")
MAIN_PATH = os.path.join(PROGRAM_PATH, "main.pyw")
SUBMENUS_PATH = os.path.join(PROGRAM_PATH, "submenus")
ADDITEMS_PATH = os.path.join(SUBMENUS_PATH, "add_items")
ADDITEMS_MENU_PATH = os.path.join(ADDITEMS_PATH, "menu.py")
ADVOPTIONS_PATH = os.path.join(SUBMENUS_PATH, "advanced_options")
ADVOPTIONS_MENU_PATH = os.path.join(ADVOPTIONS_PATH, "menu.py")
MANAGEITEMS_PATH = os.path.join(SUBMENUS_PATH, "manage_items")
MANAGEITEMS_MENU_PATH = os.path.join(MANAGEITEMS_PATH, "menu.py")

os.makedirs(LAUNCHER_PATH, exist_ok=True)
os.makedirs(SUBMENUS_PATH, exist_ok=True)
os.makedirs(ADDITEMS_PATH, exist_ok=True)
os.makedirs(ADVOPTIONS_PATH, exist_ok=True)
os.makedirs(MANAGEITEMS_PATH, exist_ok=True)

try:
    import requests
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import requests
    except Exception:
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Error", "Could not install the 'requests' module. Please, install it manually.")
        sys.exit(1)

try:
    # Icon
    link = "<link>"
    code = requests.get(link)
    with open(ICON_PATH, 'wb') as writecode:
        writecode.write(code.content)
    # Launcher Script
    link = "<link>"
    code = requests.get(link)
    with open(LAUNCHERSCRIPT_PATH, 'wb') as writecode:
        writecode.write(code.content)
    # Add Items Menu
    link = "<link>"
    code = requests.get(link)
    with open(ADDITEMS_MENU_PATH, 'wb') as writecode:
        writecode.write(code.content)
    # Advanced Options Menu
    link = "<link>"
    code = requests.get(link)
    with open(ADVOPTIONS_MENU_PATH, 'wb') as writecode:
        writecode.write(code.content)
    # Manage Items Menu
    link = "<link>"
    code = requests.get(link)
    with open(MANAGEITEMS_MENU_PATH, 'wb') as writecode:
        writecode.write(code.content)
    # Main Program
    link = "<link>"
    code = requests.get(link)
    with open(MAIN_PATH, 'wb') as writecode:
        writecode.write(code.content)
    # Run the program
    if sys.platform == 'win32':
        subprocess.Popen(f"start /B python {MAIN_PATH}", shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        os.system(f"python3 {MAIN_PATH}")    
except Exception:
    if os.path.isfile(MAIN_PATH) and os.path.isfile(ADDITEMS_MENU_PATH) and os.path.isfile(ADVOPTIONS_MENU_PATH) and os.path.isfile(MANAGEITEMS_MENU_PATH):
        if sys.platform == 'win32':
            subprocess.Popen(f"start /B python {MAIN_PATH}", shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            os.system(f"python3 {MAIN_PATH}")
    else:
        app = QApplication(sys.argv)
        QMessageBox.critical(None, "Error", "No se pudo obtener el código actualizado. Por favor, intenta de nuevo más tarde.")
        sys.exit(1)