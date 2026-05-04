# Ebook2LateX

Hệ thống chuyển đổi Ebook sang LaTeX sử dụng FastAPI, React, PostgreSQL và AI Pipeline.

## Kiến trúc (Architecture)

Hệ thống bao gồm 4 phần chính:
1. **Frontend (React)**: Giao diện người dùng hiện đại, sử dụng Vite, Axios và Lucide Icons. Cung cấp chức năng upload PDF và xem công thức.
2. **Backend (FastAPI)**: API chính xử lý logic nghiệp vụ, quản lý tài liệu và tích hợp pipeline AI.
3. **Database (PostgreSQL)**: Lưu trữ thông tin người dùng, tài liệu, công thức và log hệ thống. Quản lý bởi SQLAlchemy và Alembic.
4. **Pipeline AI**: Xử lý PDF để trích xuất các công thức toán học và chuyển đổi sang định dạng LaTeX (Mock-up).

## Cấu trúc bảng (Database Schema)
- `users`: Thông tin người dùng (admin, editor).
- `documents`: Thông tin file PDF đã upload và trạng thái xử lý.
- `formula_entries`: Các công thức LaTeX đã trích xuất từ tài liệu.
- `logs`: Ghi lại lịch sử xử lý, thời gian và độ tin cậy của AI cho từng công thức.

## Luồng chạy chuẩn (Standard Workflow)

### 1. Cấu hình Môi trường
Tạo file `.env` trong thư mục `backend/`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/ebook2latex_db
```

### 2. Khởi tạo Database & Migrate
Chạy các lệnh sau trong thư mục `backend/`:
```bash
# Cài đặt dependency
pip install -r requirements.txt

# Migrate schema lên database
alembic upgrade head
```

### 3. Seed dữ liệu mẫu
```bash
python seed.py
```

### 4. Chạy ứng dụng
**Backend:**
```bash
uvicorn main:app --reload
```

**Frontend:**
```bash
cd ../frontend
npm install
npm run dev
```

## Chức năng chính
- **Upload PDF**: Tải lên file PDF và tự động kích hoạt pipeline AI.
- **Lưu trữ thông tin**: Toàn bộ metadata của file và công thức được lưu vào PostgreSQL.
- **Log xử lý**: Ghi lại chi tiết quá trình xử lý để giám sát hiệu năng AI.
- **Tính toán nhanh**: Endpoint kiểm tra hiệu năng backend.
