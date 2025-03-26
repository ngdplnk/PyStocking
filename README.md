<p align="center">
  <img src="https://raw.githubusercontent.com/ngdplnk/PyStocking/main/assets/icon.png" alt="PyStocking Icon" width="200" />
</p>

# PyStocking - A stocking program built using Python

PyStocking is a powerful and easy-to-use stocking management tool built in Python.

## Table of Contents
- [Getting Started](#getting-started)
- [Installation](#installation)
  - [Minimum Requirements](#minimum-requirements)
  - [Windows Installation](#windows-installation)
  - [Linux Installation](#linux-installation)
- [Build PyStocking Installer (for Windows) by Yourself](#build-pystocking-installer-for-windows-by-yourself)
  - [Clone this Repository](#clone-this-repository)
  - [Install NSIS](#install-nsis)
  - [Verify Files](#verify-files)
  - [Edit .nsi file](#edit-nsi-file)
  - [Compile the Installer](#compile-the-installer)
- [Credits and Aknowledgements](#credits-and-aknowledgements)

## Getting Started
To get started with PyStocking, follow these steps:

1. Download the latest version of PyStocking from the [GitHub Releases](https://github.com/ngdplnk/PyStocking/releases/latest) page.
2. Run the installer. A shortcut should be created on your desktop and in your Windows start menu.
3. Enjoy!

## Installation  
### Minimum Requirements  
- **Operating System:**  
  - Windows 10 (64-bit - Version 10.0.14393.6796 or newer recommended).  
  - A Debian based Linux distro with a desktop environment (with kernel 5.10 or newer recommended).  
- **Processor:** 2 cores at 1.00GHz; x64 architecture.  
- **RAM:** At least 1GB.  
- **Disk Space:** Varies depending on data stored.  
- **Python:** 3.11 or newer.  

### Windows Installation
1. Download and install Python 3.11 or newer from the [official Python website](https://www.python.org/downloads/). When installing Python, be sure to select the "Add Python to PATH" option.

2. Download the latest version of PyStocking from the [GitHub Releases](https://github.com/ngdplnk/PyStocking/releases/latest) page.

3. Run the installer. A shortcut should be created on your desktop and in your Windows start menu.

4. Enjoy!

### Linux Installation
1. Install Python using apt:
    ```bash
    sudo apt update && sudo apt install -y python3 python3-venv python3-pip
    ```
2. Create a directory for PyStocking and navigate to it:
    ```bash
    mkdir -p ~/.pystocking/launcher
    cd ~/.pystocking
    ```
3. Create a virtual environment inside the PyStocking directory:
    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
5. Download the `launcher/launcher.pyw` and `requirements.txt` files from the repository:
    ```bash
    wget https://raw.githubusercontent.com/ngdplnk/PyStocking/main/launcher/launcher.pyw -P launcher/
    wget https://raw.githubusercontent.com/ngdplnk/PyStocking/main/requirements.txt
    ```
6. Install the required packages inside the virtual environment:
    ```bash
    pip install -r requirements.txt
    ```
7. Run the application:
    ```bash
    python3 launcher/launcher.pyw
    ```
8. Close the application.

Next time, you can open the program from `~/.pystocking/launcher/launcher.pyw`.

(Optional) Create a desktop shortcut:
- Create a new file `pystocking.desktop` with the following content:
    ```desktop
    [Desktop Entry]
    Name=PyStocking
    Comment=Stocking management tool
    Exec=sh -c 'source ~/.pystocking/venv/bin/activate && python3 ~/.pystocking/launcher/launcher.pyw'
    Icon=~/.pystocking/launcher/icon.png
    Terminal=false
    Type=Application
    ```
- Make the file executable:
    ```bash
    chmod +x pystocking.desktop
    ```
- Move the file to your desktop or applications directory:
    ```bash
    mv pystocking.desktop ~/Desktop/
    ```

Enjoy!

## Build PyStocking Installer (for Windows) by Yourself

You can follow these steps if you want to build the PyStocking Installer from the source code by yourself.

### Clone this Repository

First, clone/download this repository:

```bash
git clone https://github.com/ngdplnk/PyStocking.git
```

### Install NSIS

You need to install the latest NSIS (Nullsoft Scriptable Install System) version to build the installer. You can download it from [NSIS Official Website](https://nsis.sourceforge.io/Download). Be sure to follow the on-screen instructions to complete the installation.

### Verify Files

Navigate to the cloned repository folder and ensure that you have the following files:

- `launcher\build.nsi`
- `launcher\icon.ico`
- `launcher\launcher.pyw`
- `submenus\add_items\menu.py`
- `submenus\advanced_options\menu.py`
- `submenus\manage_items\menu.py`
- `requirements.txt`
- `main.pyw`

If any of these files are missing, please download them directly from the repository.

### Edit .nsi File

Open the `build.nsi` file in a text editor and replace the placeholders `<TYPE THE XXXX PATH HERE>` with the actual paths to your files/folders. Save the changes.

### Compile the Installer

1. Open NSIS.
2. Select the option "Compile NSI Scripts".
3. Drag and drop the `build.nsi` file into the NSIS window.
4. An installer for PyStocking will be created.
5. Enjoy!

## Credits and Aknowledgements

**PyStocking is an independent software and is not affiliated with any third-party brands or services.**

Special thanks to [@Bruno-Machuca](https://github.com/Bruno-Machuca) for testing and providing feedback on the program :shipit:

PyStocking uses <a href="https://www.flaticon.com/free-icons/stock" title="'Stock' Icons on Flaticon">'Ready Stock' icon created by Hilmy Abiyyu A. - Flaticon</a> - Licensed under the [Flaticon License](https://www.flaticon.com/legal#nav-flaticon-agreement)

PyStocking is licensed under [Elastic License 2.0](https://github.com/ngdplnk/PyStocking/blob/main/LICENSE) - Copyright © 2025 ngdplnk