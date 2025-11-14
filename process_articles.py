import json
import re
from pathlib import Path
from langdetect import detect, LangDetectException

RAW_FILE = Path("raw_articles.json")
CLEAN_FILE = Path("cleaned_articles.json")

def load_raw_articles():
    if not RAW_FILE.exists():
        raise FileNotFoundError("raw_articles.json not found. Run fetch_news.py first.")
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def classify_topic(text):
    text = text.lower()
    if any(k in text for k in ["sports", "match", "cricket", "tournament", "player"]):
        return "Sports"
    elif any(k in text for k in ["crime", "police", "murder", "attack", "theft", "arrest"]):
        return "Crime"
    elif any(k in text for k in ["government", "election", "minister", "parliament", "policy"]):
        return "Politics"
    elif any(k in text for k in ["tech", "software", "ai", "startup", "innovation", "data"]):
        return "Technology"
    elif any(k in text for k in ["movie", "film", "actor", "music", "celebrity", "show"]):
        return "Entertainment"
    else:
        return "General"

def process_articles(data):
    seen = set()
    cleaned = []
    for art in data:
        title = art.get("title", "").strip()
        url = art.get("url")
        content = art.get("content") or art.get("description") or ""
        content = clean_text(content)

        if url in seen or not title:
            continue
        seen.add(url)

        lang = detect_language(content or title)
        if lang != "en":
            continue

        topic = classify_topic(content)

        cleaned.append({
            "title": title,
            "url": url,
            "source": art.get("source", {}).get("name"),
            "content": content,
            "topic": topic,
        })
    return cleaned

def save_cleaned(cleaned):
    with open(CLEAN_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(cleaned)} cleaned & classified articles → {CLEAN_FILE}")

def main():
    print("Processing raw_articles.json ...")
    raw = load_raw_articles()
    cleaned = process_articles(raw)
    save_cleaned(cleaned)

if __name__ == "__main__":
    main()
