import os
import subprocess

HOME = os.path.expanduser('~')
hidden_script = os.path.join(HOME, '.local', 'bin', '.syskey.py')
desktop_file = os.path.join(HOME, '.config', 'autostart', 'syskey.desktop')
nohup_file = os.path.join(HOME, 'nohup.out')

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
if os.path.exists(nohup_file):
    os.remove(nohup_file)

print("Keylogger stopped, autostart entry and nohup.out removed.") 