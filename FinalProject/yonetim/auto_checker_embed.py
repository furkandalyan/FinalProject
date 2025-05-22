import threading
import time
from yonetim.notification_jobs import check_old_tasks_and_notify

def background_loop():
    while True:
        print("🔁 Auto-checking notifications...")
        check_old_tasks_and_notify()
        print("✅ Done.")
        time.sleep(60)

def start_background_checker():
    thread = threading.Thread(target=background_loop, daemon=True)
    thread.start()
    print("🚀 Background checker başlatıldı.")
