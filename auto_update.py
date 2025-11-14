import os
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

def run_pipeline():
    print("🚀 Running update pipeline...")
    try:
        subprocess.run(["python", "fetch_news.py"], check=True)
        subprocess.run(["python", "process_articles.py"], check=True)
        subprocess.run(["python", "summarize_sentiment.py"], check=True)
        print("✅ Pipeline completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Pipeline failed: {e}\n")

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, "interval", hours=3, id="update_job")
    print("🕓 Auto-update service started. Runs every 3 hours.")
    run_pipeline()  
    scheduler.start()

if __name__ == "__main__":
    main()
