import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tải biến môi trường từ .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Đối với PostgreSQL, SQLAlchemy yêu cầu tiền tố postgresql://
# Nếu trong .env là postgresql+psycopg2:// thì càng tốt, nếu không chúng ta có thể điều chỉnh ở đây.
if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
