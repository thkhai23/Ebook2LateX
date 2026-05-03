from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import document
from app.database import engine
from app import models

# Khởi tạo FastAPI
app = FastAPI(
    title="Ebook2LateX API",
    description="Backend API cho ứng dụng chuyển đổi Ebook sang LaTeX",
    version="0.1.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trong thực tế nên giới hạn lại
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(document.router)

@app.get("/")
def read_root():
    return {"message": "Chao mung ban den voi Ebook2LateX!"}

@app.get("/multiply/{number}")
def multiply_by_ten(number: int):
    result = number * 10
    return {
        "input": number,
        "multiplied_by": 10,
        "result": result
    }

@app.get("/shoes/{brand}/{size}")
def buy_shoes(brand: str, size: int):
    return {
        "message": f"Bạn muốn mua giày {brand} kích thước {size} đúng không?"
    }
