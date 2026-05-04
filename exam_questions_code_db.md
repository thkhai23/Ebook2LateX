# BỘ CÂU HỎI PHẢN BIỆN: CHIÊN SÂU CODE & POSTGRESQL

Tài liệu này giả định các tình huống Giảng viên xoáy sâu vào kỹ thuật để kiểm tra xem bạn có thực sự hiểu code hay không.

---

## NHÓM 1: CƠ SỞ DỮ LIỆU (POSTGRESQL & SQLALCHEMY)

### Câu 1: Tại sao em lại chọn kiểu dữ liệu UUID cho khóa chính thay vì Integer tự tăng?
- **Trả lời**: 
    1. **Bảo mật**: ID tự tăng (1, 2, 3...) cho phép người dùng đoán được ID của tài liệu khác bằng cách thay đổi con số trên URL. UUID là chuỗi ngẫu nhiên, không thể đoán được.
    2. **Phân tán**: Nếu sau này hệ thống mở rộng ra nhiều máy chủ, dùng UUID đảm bảo không bao giờ bị trùng khóa chính khi gộp dữ liệu.

### Câu 2: Trong file `models.py`, tôi thấy em dùng `ondelete='CASCADE'`. Nó có ý nghĩa gì?
- **Trả lời**: Đây là ràng buộc toàn vẹn dữ liệu. Khi em xóa một bản ghi ở bảng cha (ví dụ xóa 1 Document), PostgreSQL sẽ tự động xóa tất cả các bản ghi liên quan ở bảng con (ví dụ các FormulaEntries của tài liệu đó). Nếu không có cái này, Database sẽ bị rác hoặc lỗi "vi phạm khóa ngoại".

### Câu 3: Kiểu dữ liệu `JSONB` trong bảng `Logs` khác gì với `JSON` thông thường?
- **Trả lời**: `JSONB` lưu trữ dữ liệu dưới dạng nhị phân đã được phân tích cú pháp (parsed). Nó giúp truy vấn nhanh hơn và hỗ trợ đánh Index trên các trường bên trong JSON, trong khi `JSON` thông thường chỉ là lưu một chuỗi văn bản đơn thuần.

### Câu 4: Làm thế nào để đảm bảo mật khẩu người dùng không bị lộ nếu Database bị hack?
- **Trả lời**: Em không lưu mật khẩu thô. Em sử dụng thư viện `bcrypt` để băm (hash) mật khẩu kèm theo "salt". Ngay cả admin hệ thống cũng không biết mật khẩu thực sự của người dùng là gì.

---

## NHÓM 2: LẬP TRÌNH BACKEND (FASTAPI & PYTHON)

### Câu 5: Lệnh `db: Session = Depends(get_db)` trong các Router có ý nghĩa gì?
- **Trả lời**: Đây là kỹ thuật **Dependency Injection** (Tiêm phụ thuộc). FastAPI sẽ tự động mở một phiên kết nối Database (`Session`) khi có request đến, đưa vào hàm để em dùng, và tự động đóng kết nối đó khi request kết thúc để tránh rò rỉ bộ nhớ.

### Câu 6: Tại sao em lại tách biệt `crud.py` và `routers/` ra riêng?
- **Trả lời**: Đây là mô hình phân lớp. `crud.py` chỉ lo việc tương tác DB, còn `routers/` lo việc điều hướng và kiểm tra dữ liệu đầu vào. Việc tách biệt giúp code dễ bảo trì, dễ viết test và có thể tái sử dụng các hàm CRUD ở nhiều nơi khác nhau.

### Câu 7: Middleware CORS trong file `main.py` dùng để làm gì?
- **Trả lời**: Theo mặc định, trình duyệt sẽ chặn các yêu cầu từ một tên miền khác (ví dụ từ React chạy cổng 5173 gọi tới FastAPI cổng 8000). CORS giúp ta "cấp phép" cho Frontend được quyền truy cập vào các tài nguyên của Backend.

### Câu 8: `Pydantic` (file `schemas.py`) đóng vai trò gì trong dự án?
- **Trả lời**: Nó đóng vai trò là "người gác cổng". Nó kiểm tra xem dữ liệu người dùng gửi lên có đúng kiểu không (ví dụ: email có đúng định dạng không, mật khẩu có đủ độ dài không). Nếu sai, nó sẽ trả về lỗi ngay lập tức mà không cần chạy vào logic bên trong.

---

## NHÓM 3: QUY TRÌNH VẬN HÀNH (ALEMBIC & GIT)

### Câu 9: Nếu tôi thay đổi một cột trong bảng, tôi cần làm gì để Database cập nhật?
- **Trả lời**: 
    1. Sửa Class trong `models.py`.
    2. Chạy `alembic revision --autogenerate` để tạo file script migration.
    3. Chạy `alembic upgrade head` để áp dụng thay đổi đó vào PostgreSQL.

### Câu 10: File `__init__.py` trong thư mục `app/` để làm gì? Có thể xóa nó không?
- **Trả lời**: Không nên xóa. Nó đánh dấu thư mục đó là một **Python Package**. Nhờ có nó mà em có thể viết lệnh `from app.models import Base` từ các thư mục khác.

---
**Lời khuyên**: Khi trả lời, hãy nhìn thẳng vào giảng viên, trả lời tự tin và nếu có thể, hãy mở trực tiếp đoạn code liên quan để minh chứng.
