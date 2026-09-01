# 📈 NewsPulse ML

**NewsPulse ML** is an end-to-end asynchronous data pipeline designed to ingest financial news and automatically analyze market sentiment using Artificial Intelligence. This project demonstrates a production-ready architecture covering data extraction, ML processing, database management, and visualization.

---

## 🛠 Tech Stack
* **Language:** Python 3.11
* **Database:** SQLite + SQLAlchemy 2.0 (ORM)
* **Machine Learning:** HuggingFace `transformers`, FinBERT (ProsusAI)
* **Analytics & UI:** Streamlit, Pandas
* **Infrastructure:** Docker, Docker Compose

---

## 🚀 Key Features & Workflow

1. **Data Ingestion:** Fetches the latest financial market news via external API.
2. **ML Processing:** A background worker uses the FinBERT NLP model to analyze news headlines and compute sentiment scores (bullish/bearish).
3. **Storage:** Safely stores raw articles and calculated metrics in a relational database with strict SQLAlchemy 2.0 typing.
4. **Visualization:** Interactive Streamlit dashboard to monitor real-time market sentiment and aggregated trends.

---

## 📦 Quick Start (Docker)

Make sure Docker and Docker Compose are running on your system.

1. Build and run containers in background mode:
```bash
docker compose up --build -d
```

2. Open the dashboard in your browser:
```text
http://localhost:8501
```

---

## ⚙️ Manual Execution (Local Environment)

If you prefer running the pipeline components individually:

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run data ingestion:**
```bash
python3 -m src.ingestion.news_api
```

3. **Run ML sentiment analyzer:**
```bash
python3 -m src.worker.analyzer
```

4. **Launch dashboard:**
```bash
streamlit run src/dashboard/app.py
```