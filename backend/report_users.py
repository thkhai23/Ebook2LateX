from sqlalchemy import func
from database import SessionLocal
from app.models import User, Document

def report_users():
    db = SessionLocal()
    try:
        # Truy vấn User kèm theo số lượng tài liệu (sử dụng outerjoin để lấy cả người có 0 tài liệu)
        results = (
            db.query(
                User.full_name, 
                User.username_email, 
                func.count(Document.id).label("doc_count")
            )
            .outerjoin(Document, User.user_id == Document.user_id)
            .group_by(User.user_id)
            .all()
        )

        print("\n--- BAO CAO THONG KE NGUOI DUNG ---")
        print(f"{'Ho ten':<25} | {'Email':<30} | {'So tai lieu'}")
        print("-" * 75)
        
        for name, email, count in results:
            display_name = name if name else "Chua cap nhat"
            print(f"{display_name:<25} | {email:<30} | {count}")
        print("-" * 75)
        print(f"Tong so User: {len(results)}\n")

    except Exception as e:
        print(f"Co loi xay ra: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    report_users()
