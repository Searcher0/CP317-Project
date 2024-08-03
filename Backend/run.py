import threading
import time
from scraper.run_scrapers import run_all_scrapers
from api.app import app


def run_scrapers_periodically():
    while True:
        # run_all_scrapers()
        time.sleep(24 * 3600)  # Run every 24 hours

if __name__ == "__main__":
    scraper_thread = threading.Thread(target=run_scrapers_periodically)
    scraper_thread.start()
    
    try:
        app.run(port=5001)  # Start the Flask app on port 5001
    except OSError:
        print("Port 5001 is in use, please choose another port.")