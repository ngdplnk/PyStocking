<p align="center">
  <img src="https://raw.githubusercontent.com/ngdplnk/PyStocking/main/launcher/icon.png" alt="PyStocking Icon" width="200" />
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
- [Credits](#credits)

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
2. Clone this repository:
    ```bash
    git clone https://github.com/ngdplnk/PyStocking.git
    ```
3. Navigate to the cloned repository:
    ```bash
    cd PyStocking
    ```
4. Create and activate a virtual environment inside the cloned repo folder:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
5. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
6. Run the application (make sure to activate the virtual environment first):
    ```bash
    source venv/bin/activate
    python3 launcher/launcher.pyw
    ```
7. (Optional) Create a desktop shortcut:
    - Create a new file `pystocking.desktop` with the following content:
        ```desktop
        [Desktop Entry]
        Name=PyStocking
        Comment=Stocking management tool
        Exec=sh -c 'cd /path/to/cloned/repo && source venv/bin/activate && python3 launcher/launcher.pyw'
        Icon=/path/to/cloned/repo/launcher/icon.png
        Terminal=false
        Type=Application
        ```
    - Replace `/path/to/cloned/repo` with the actual path.
    - Make the file executable:
        ```bash
        chmod +x pystocking.desktop
        ```
    - Move the file to your desktop or applications directory:
        ```bash
        mv pystocking.desktop ~/Desktop/
        ```
8. Enjoy!

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

Navigate to the cloned repository and ensure that you have the following files:

- `launcher\build.nsi`
- `launcher\icon.ico`
- `launcher\launcher.pyw`
- `submenus\add_items\menu.py`
- `submenus\advanced_options\menu.py`
- `submenus\manage_items\menu.py`
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

## Credits

**PyStocking is an independent software and is not affiliated with any third-party brands or services.**

Licensed under [Elastic License 2.0](https://github.com/ngdplnk/PyStocking/blob/main/LICENSE) - Copyright © 2025 ngdplnk