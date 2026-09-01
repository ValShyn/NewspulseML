import time
import requests
from datetime import datetime
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

from src.config import NEWS_API_KEY
from src.database.connection import SessionLocal
from src.database.model import Article


TOPICS = ["bitcoin", "ethereum", "artificial intelligence", "tesla", "apple"]


def fetch_new_producer(topic: str, q: queue.Queue):
    """
    Fetches new articles for a given topic and puts them into the queue.
    """
    print(f"[{topic}] 📡 Starting to fetch news...")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": topic,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,  # Берем 10 свежих новостей по теме
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])

        for article in articles:
            q.put(article)

        print(f"[{topic}] ✅ Find {len(articles)} articles. Adding to queue...")

    except requests.RequestException as e:
        print(f"[{topic}] ❌ Error fetching news from NewsAPI: {e}")


def save_news_articles(q: queue.Queue):
    """
    Saves articles from the queue to the database
    """
    print("💾 Starting to save articles to the database...")

    db = SessionLocal()  # Open a new database session

    saved_count = 0

    while True:
        item = q.get()  # Get an article from the queue

        if item == "STOP":
            print("💾 Stopping the saving process.")
            break
        exists = db.query(Article).filter(Article.url == item["url"]).first()

        if not exists:
            raw_date = item.get("publishedAt")
            published_dt = None

            if raw_date:
                try:
                    published_dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                except ValueError:
                    print(f"⚠️ Invalid date format for article '{item['title']}': {raw_date}")

            new_article = Article(
                title=item["title"],
                url=item["url"],
                published_at=published_dt,
                status="pending"
            )
            db.add(new_article)
            db.commit()
            saved_count += 1
        q.task_done()
    db.close()

    return f"💾 Finished saving articles. Total saved: {saved_count}"


def run_ingestion_pipeline():

    start_time = time.time()

    news_queue = queue.Queue()

    # Start the consumer thread
    consumer_thread = threading.Thread(target=save_news_articles, args=(news_queue, ))
    consumer_thread.start()

    with ThreadPoolExecutor(max_workers=5) as executor:
        for topic in TOPICS:
            executor.submit(fetch_new_producer, topic, news_queue)

    news_queue.put("STOP")  # Signal the consumer to stop

    consumer_thread.join()  # Wait for the consumer thread to finish

    consumer_thread.join()  # Wait for the consumer thread to finish
    print(f"⏱ Total time taken: {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    run_ingestion_pipeline()
