import uuid
from app.database import SessionLocal
from app.models import User, Document, FormulaEntry, Log

def seed_data():
    # 1. Khởi tạo phiên làm việc (Session)
    db = SessionLocal()
    
    try:
        print("Dang tao du lieu...")

        # 2. Tạo dữ liệu cho bảng User
        test_user = User(
            user_id=uuid.uuid4(),
            username_email="admin@ebook2latex.com",
            password_hash="admin123", # Plain text for demo, use hash in production
            full_name="System Administrator",
            role="Admin"
        )
        db.add(test_user)
        db.flush()

        # 3. Tạo dữ liệu mẫu cho bảng Documents
        test_doc = Document(
            id=uuid.uuid4(),
            user_id=test_user.user_id,
            file_name="Giao_trinh_Toan_12.pdf",
            file_path_url="/uploads/toan12.pdf",
            status="Completed"
        )
        db.add(test_doc)
        db.flush()

        # 4. Tạo dữ liệu mẫu cho bảng FormulaEntries
        formula = FormulaEntry(
            id=uuid.uuid4(),
            document_id=test_doc.id,
            latex_content=r"\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            order_index=1
        )
        db.add(formula)
        db.flush()

        # 5. Tạo dữ liệu mẫu cho bảng Log
        log_entry = Log(
            log_id=uuid.uuid4(),
            formula_id=formula.id,
            processing_time_ms=1250,
            confidence_score=0.97,
            environment_info={"device": "cpu", "version": "v1.0"}
        )
        db.add(log_entry)

        # 6. Xác nhận lưu toàn bộ thay đổi vào Database
        db.commit()
        print("Tao du lieu thanh cong!")

    except Exception as e:
        print(f"Co loi xay ra: {e}")
        db.rollback() # Hoàn tác nếu có lỗi để tránh rác dữ liệu
    finally:
        db.close() # Luôn đóng kết nối sau khi xong

if __name__ == "__main__":
    seed_data()
