import os
import json
import requests
import sys
from dotenv import load_dotenv

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if not NEWSAPI_KEY:
    raise SystemExit("❌ ERROR: Set NEWSAPI_KEY in .env before running.")

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
OUT_FILE = "raw_articles.json"


def fetch_headlines(country=None, query=None, page_size=100, max_pages=2):
    """
    Fetch global or country-specific news with optional topic (query).
    Example: fetch_headlines(query='health') -> global health news
    """
    all_articles = []

    for page in range(1, max_pages + 1):
        params = {
            "apiKey": NEWSAPI_KEY,
            "language": "en",
            "pageSize": page_size,
            "page": page,
        }

        if country:
            params["country"] = country
        if query:
            params["q"] = query 

        print(
            f"🌍 Fetching page {page}/{max_pages}"
            f"{' globally' if not country else f' for {country.upper()}'}"
            f"{' about ' + query if query else ''} ..."
        )

        resp = requests.get(NEWSAPI_URL, params=params, timeout=20)
        if resp.status_code != 200:
            print("⚠️ Error:", resp.text)
            break

        data = resp.json()
        articles = data.get("articles", [])
        if not articles:
            break

        all_articles.extend(articles)
        print(f"✅ Retrieved {len(articles)} articles from page {page}")

    print(f"💾 Total collected: {len(all_articles)} articles")
    return all_articles


def save_raw(articles, filename=OUT_FILE):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved {len(articles)} articles → {filename}")


def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else None
    if topic and topic.lower() == "general":
        print("🗞️ Fetching all top headlines globally (no filter)...")
        articles = fetch_headlines(page_size=50, max_pages=2)
    else:
        print(f"🗞️ Fetching global news for topic: {topic or 'general'}")
        articles = fetch_headlines(query=topic, page_size=50, max_pages=2)

    save_raw(articles)



if __name__ == "__main__":
    main()
