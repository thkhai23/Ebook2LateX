# GIẢI THÍCH CHI TIẾT TOÀN BỘ FILE TRONG DỰ ÁN EBOOK2LATEX

Tài liệu này cung cấp cái nhìn chi tiết nhất về mọi tệp tin có trong dự án, giúp bạn nắm vững cấu trúc hệ thống từ Backend đến Frontend.

---

## 1. THƯ MỤC GỐC (ROOT)

- **`.git/`**: Thư mục ẩn chứa toàn bộ lịch sử quản lý mã nguồn của Git. Đừng bao giờ xóa thư mục này.
- **`.gitignore`**: Danh sách các file và thư mục mà Git nên bỏ qua (không đẩy lên mạng). Thường bao gồm `node_modules/`, `venv/`, và các file cấu hình bảo mật như `.env`.
- **`README.md`**: File hướng dẫn sử dụng dự án bằng ngôn ngữ Markdown. Đây là bộ mặt của dự án trên GitHub.
- **`Tong_hop_Kien_thuc_Ebook2LateX.txt`**: File tổng hợp kiến thức từ các bài blog để bạn ôn tập và trả lời phản biện.
- **`ebook2latex_architecture_walkthrough.md`**: Chính là file tài liệu này.
- **`requirements.txt`**: Danh sách các thư viện Python cần thiết cho toàn bộ dự án.
- **`venv/`**: Thư mục môi trường ảo của Python. Chứa trình thông dịch Python và các thư viện đã cài đặt riêng cho dự án này.

---

## 2. THƯ MỤC BACKEND (MÁY CHỦ & DỮ LIỆU)

### 📁 Thư mục `backend/`
- **`.env`**: Lưu thông tin cấu hình nhạy cảm (như `DATABASE_URL`).
- **`alembic.ini`**: File cấu hình chính của Alembic (công cụ quản lý migration database).
- **`main.py`**: File chạy chính của ứng dụng. Nó khởi tạo FastAPI, gộp các router và cấu hình CORS.
- **`database.py`**: Chứa code khởi tạo kết nối cơ bản tới DB.
- **`data.json`**: File chứa dữ liệu mẫu định dạng JSON để phục vụ việc seeding.
- **`seed.py` / `seed_faker.py` / `seed_from_json.py`**: Các script dùng để nạp dữ liệu mẫu vào database theo các cách khác nhau (nhập tay, ngẫu nhiên, hoặc từ file JSON).
- **`search_formulas.py` / `report_users.py`**: Các script tiện ích để truy vấn nhanh dữ liệu hoặc tạo báo cáo thống kê.
- **`requirements.txt`**: Danh sách thư viện riêng cho phần backend.
- **`uploads/`**: Thư mục lưu trữ các file PDF mà người dùng tải lên hệ thống.

### 📁 Thư mục `backend/app/` (Logic lõi)
- **`__init__.py`**: File đánh dấu thư mục `app` là một package Python, cho phép các file khác import lẫn nhau.
- **`database.py`**: Quản lý việc tạo Engine và Session để thao tác với PostgreSQL.
- **`models.py`**: Định nghĩa các "Bảng" dữ liệu dưới dạng Class (ORM). Đây là xương sống của cơ sở dữ liệu.
- **`schemas.py`**: Định nghĩa kiểu dữ liệu đầu vào/đầu ra cho API (Pydantic models), giúp kiểm tra tính hợp lệ của dữ liệu.
- **`crud.py`**: Chứa các hàm Create-Read-Update-Delete. Tách biệt logic xử lý dữ liệu khỏi logic giao diện API.
- **`ai_pipeline.py`**: Chứa logic xử lý PDF và trích xuất LaTeX (hiện đang dùng hàm giả lập hoặc tích hợp OCR).

### 📁 Thư mục `backend/app/routers/`
- **`document.py`**: Chứa các endpoint API liên quan đến tài liệu (upload, danh sách, xóa).
- **`user.py`**: Chứa các endpoint API liên quan đến người dùng (đăng ký, thông tin).

### 📁 Thư mục `backend/migrations/`
- **`env.py`**: Cấu hình môi trường chạy cho Alembic.
- **`script.py.mako`**: File mẫu để Alembic tạo ra các bản migration mới.
- **`versions/`**: Chứa các file python đánh số thứ tự, mỗi file là một bước thay đổi cấu trúc Database.

---

## 3. THƯ MỤC FRONTEND (GIAO DIỆN NGƯỜI DÙNG)

### 📁 Thư mục `frontend/`
- **`index.html`**: File HTML chính của ứng dụng. Là nơi React được "nhúng" vào.
- **`package.json`**: Quản lý thông tin dự án, các thư viện JavaScript và các câu lệnh chạy (`npm run dev`).
- **`vite.config.js`**: Cấu hình cho Vite - công cụ biên dịch frontend siêu tốc.
- **`eslint.config.js`**: Cấu hình kiểm tra lỗi cú pháp JavaScript.
- **`.env`**: Lưu URL của backend API để frontend biết chỗ mà gọi.
- **`node_modules/`**: Chứa hàng ngàn thư viện JavaScript đã tải về. Đừng bao giờ đụng vào đây.

### 📁 Thư mục `frontend/src/` (Mã nguồn giao diện)
- **`main.jsx`**: Điểm bắt đầu của ứng dụng React.
- **`App.jsx`**: Component chính chứa toàn bộ giao diện và logic của trang web.
- **`App.css` / `index.css`**: Chứa mã nguồn CSS để trang trí giao diện (Dark Mode, Glassmorphism).
- **`assets/`**: Chứa hình ảnh, logo và các file tĩnh khác.
- **`components/`**: (Nếu có) Chứa các thành phần giao diện nhỏ có thể tái sử dụng.

---

## 4. CÁC ĐIỂM CẦN LƯU Ý KHI TRÌNH BÀY
1. **Tại sao có nhiều file `__init__.py`?** -> Để biến thư mục thành "Module", giúp code được tổ chức ngăn nắp và có thể gọi qua lại dễ dàng.
2. **Tại sao có nhiều file `requirements.txt`?** -> Một cái ở gốc để cài nhanh toàn bộ, một cái ở backend để phục vụ đóng gói Docker sau này.
3. **Tại sao cần `.env`?** -> Để tách biệt cấu hình và mã nguồn. Giúp thay đổi Database dễ dàng mà không cần sửa code.

---
**Người soạn thảo: Antigravity AI - 2026**
