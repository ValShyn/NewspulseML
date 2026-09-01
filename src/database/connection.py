from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL

from src.database.model import Base

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    print("🛠 Создание таблиц в базе данных...")
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("✅ База данных успешно инициализирована!")