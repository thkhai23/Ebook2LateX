import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Tải các biến môi trường từ tập tin .env
load_dotenv()

# 1. Lấy chuỗi kết nối từ biến môi trường
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Đối với PostgreSQL, SQLAlchemy yêu cầu tiền tố postgresql+psycopg2://
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

# 2. Tạo Engine: Đây là "nguồn" kết nối chính tới Database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Tạo SessionLocal: Mỗi thực thể của lớp này sẽ là một phiên làm việc database
# autocommit=False: Đảm bảo dữ liệu chỉ được lưu khi ta ra lệnh commit()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Tạo Base class: Các models (User, Document...) sẽ kế thừa từ đây
Base = declarative_base()

# 5. Dependency: Tao va dong session cho moi request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
