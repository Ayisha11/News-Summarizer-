import json
from pathlib import Path
from transformers import pipeline

CLEAN_FILE = Path("cleaned_articles.json")
OUT_FILE = Path("processed.json")

def load_cleaned():
    if not CLEAN_FILE.exists():
        raise FileNotFoundError("cleaned_articles.json not found. Run process_articles.py first.")
    with open(CLEAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    print("Loading summarization and sentiment models...")

    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    sentiment_analyzer = pipeline("sentiment-analysis")

    articles = load_cleaned()
    processed = []

    for art in articles:
        content = art.get("content", "")
        if not content.strip():
            continue
        try:
            text_for_sum = content[:2000]  
            summary = summarizer(text_for_sum, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
        except Exception:
            summary = content[:300] + "..."

        try:
            sent = sentiment_analyzer(summary)[0]
        except Exception:
            sent = {"label": "neutral", "score": 0.0}

        processed.append({
            "title": art["title"],
            "source": art["source"],
            "summary": summary,
            "sentiment": sent,
            "url": art["url"]
        })
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(processed)} summarized + sentiment-labeled articles → {OUT_FILE}")

if __name__ == "__main__":
    main()
