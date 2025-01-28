import sys
import os

if sys.platform == "win32":
    PROGRAM_PATH = os.path.join(os.getenv('APPDATA'), 'PyStocking')
else:
    PROGRAM_PATH = os.path.join(os.path.expanduser('~'), '.pystocking')

# Delete program folder and all its contents
try:
    os.system(f"rm -rf {PROGRAM_PATH}")
except Exception as e:
    print(e)
