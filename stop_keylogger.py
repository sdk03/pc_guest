import os
import subprocess

HOME = os.path.expanduser('~')
hidden_script = os.path.join(HOME, '.local', 'bin', '.syskey.py')
desktop_file = os.path.join(HOME, '.config', 'autostart', 'syskey.desktop')

# Kill running keylogger processes
try:
    subprocess.run(['pkill', '-f', hidden_script], check=False)
except Exception:
    pass

# Remove files
if os.path.exists(hidden_script):
    os.remove(hidden_script)
if os.path.exists(desktop_file):
    os.remove(desktop_file)

print("Keylogger stopped and autostart entry removed.") 