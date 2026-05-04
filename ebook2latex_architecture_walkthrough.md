# KIẾN TRÚC DỰ ÁN EBOOK2LATEX (PHẦN BACKEND)

Tài liệu này giải thích ý nghĩa của từng file và các lưu ý quan trọng khi vận hành hệ thống.

---

## 1. CẤU TRÚC THƯ MỤC VÀ Ý NGHĨA TỪNG FILE

### 📁 Thư mục gốc (Root)
- **`.env`**: Nơi lưu trữ "bí mật" của dự án (Database URL, API Key). File này không được đẩy lên GitHub để bảo mật.
- **`requirements.txt`**: Danh sách tất cả các thư viện cần thiết. Dùng lệnh `pip install -r requirements.txt` để cài đặt nhanh.
- **`Tong_hop_Kien_thuc_Ebook2LateX.txt`**: File tài liệu tổng hợp kiến thức từ các bài blog để phục vụ báo cáo.

### 📁 Thư mục `backend/app/` (Lõi ứng dụng)
- **`database.py`**: 
    - Khởi tạo **Engine** (đường ống kết nối tới PostgreSQL).
    - Tạo **SessionLocal** (phiên làm việc). Mỗi khi cần thêm/sửa/xóa dữ liệu, ta mở một Session từ đây.
- **`models.py`**: 
    - Định nghĩa cấu trúc các bảng (ORM). 
    - Đây là nơi quy định kiểu dữ liệu (UUID, String, Integer) và các mối quan hệ (ForeignKey).
- **`crud.py`**: 
    - Chứa các hàm nghiệp vụ (Create, Read, Update, Delete). 
    - Ví dụ: Hàm lấy danh sách tài liệu, hàm lưu công thức mới.
- **`routers/`**: 
    - Chia nhỏ các API theo từng nhóm (ví dụ: `document.py` quản lý upload, `user.py` quản lý đăng nhập). Giúp code gọn gàng hơn.

### 📁 Thư mục `backend/migrations/` (Quản lý DB)
- **`env.py`**: File cấu hình của Alembic. Lưu ý quan trọng nhất là dòng `target_metadata = Base.metadata` giúp Alembic "thấy" được các bảng bạn định nghĩa trong `models.py`.
- **`versions/`**: Chứa các file script migration. Mỗi file đại diện cho một lần thay đổi cấu trúc Database.

### 📄 Các file thực thi khác
- **`main.py`**: Điểm bắt đầu của ứng dụng FastAPI. Nơi gộp các Router lại và cấu hình Middleware (như CORS).
- **`seed.py`**: Script "gieo hạt" dữ liệu mẫu. Giúp bạn có ngay dữ liệu để demo mà không cần nhập tay.

---

## 2. CÁC LƯU Ý "SỐNG CÒN" KHI KẾT NỐI DATABASE

### ⚠️ Driver kết nối
SQLAlchemy không thể kết nối trực tiếp bằng URL `postgresql://`. Nó cần một driver trung gian là **psycopg2**. Vì vậy, chuỗi kết nối luôn phải có dạng:
`postgresql+psycopg2://user:password@localhost:5432/dbname`

### ⚠️ Quản lý Phiên làm việc (Session)
Luôn tuân thủ quy tắc: **Mở -> Dùng -> Đóng**.
```python
db = SessionLocal()
try:
    # Thao tác dữ liệu
    db.commit()
finally:
    db.close() # Rất quan trọng để tránh treo Database
```

### ⚠️ Quan hệ bảng (Relationship)
- **Cascade Delete**: Trong dự án này, bảng `formula_entries` được cấu hình `ondelete='CASCADE'`. Nghĩa là nếu bạn xóa một Document, PostgreSQL sẽ tự dọn dẹp toàn bộ công thức liên quan. Bạn không cần xóa thủ công từng cái.

---

## 3. QUY TRÌNH PHÁT TRIỂN CHUẨN
1. Sửa cấu trúc bảng trong `models.py`.
2. Chạy `alembic revision --autogenerate -m "mô tả thay đổi"`.
3. Kiểm tra file script vừa tạo trong thư mục `versions/`.
4. Chạy `alembic upgrade head` để áp dụng vào DB.
5. (Tùy chọn) Chạy `seed.py` để nạp dữ liệu test mới.

---
**Người soạn thảo: Antigravity AI - 2026**
