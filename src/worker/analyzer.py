from transformers import pipeline
from src.database.connection import SessionLocal
from src.database.model import Article


def analyze_news():
    """
    Analyzes the sentiment of news articles in the database that have a 'pending' status.
    Updates the sentiment score and changes the status to 'analyzed'.
    """
    print("🧠 Starting sentiment analysis...")

    sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    db = SessionLocal()  # Open a new database session

    pending_articles = db.query(Article).filter(Article.status == "pending").all()

    if not pending_articles:
        print("🧠 No pending articles found for analysis.")
        db.close()
        return

    print(f"🧠 Found {len(pending_articles)} pending articles. Analyzing...")

    for article in pending_articles:
        result = sentiment_analyzer(article.title)[0]
        label = result['label']
        score = result['score']

        if label == "negative":
            sentiment_score = -score
        elif label == "positive":
            sentiment_score = score
        else:  # label == "neutral"
            sentiment_score = 0.0

        article.sentiment = round(sentiment_score, 4)
        article.status = "processed"

        print(f"[{label.upper():>8}] {article.title[:60]}...")

    db.commit()
    db.close()
    print("🧠 Sentiment analysis completed and database updated.")


if __name__ == "__main__":
    analyze_news()
    