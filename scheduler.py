import schedule
import time
import subprocess
import datetime

def job():
    print(f"⏰ Timer Triggered at {datetime.datetime.now()}")
    print("🚀 Running Growzix TikTok Automation...")
    subprocess.run(["python", "main.py"])

# USA EST Schedule
# Note: Ensure your system clock is set correctly or adjust these for your timezone.
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("12:00").do(job)
schedule.every().day.at("18:00").do(job)
schedule.every().day.at("21:00").do(job)

print("⏳ Scheduler is running... Keeping watch for USA EST posting times.")
print("Schedule: 8AM, 12PM, 6PM, 9PM.")

while True:
    schedule.run_pending()
    time.sleep(60) # Check every minute
