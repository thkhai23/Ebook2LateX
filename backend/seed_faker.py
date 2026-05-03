import uuid
import random
from faker import Faker
from database import SessionLocal
from app.models import User, Document

# Khởi tạo Faker
fake = Faker()

def seed_faker():
    db = SessionLocal()
    try:
        print("Dang bat dau gieo du lieu voi Faker...")
        
        for _ in range(50):
            # 1. Tao User ngau nhien
            user = User(
                user_id=uuid.uuid4(),
                username_email=fake.unique.email(),
                password_hash="pbkdf2:sha256:default_hash",
                full_name=fake.name(),
                role=random.choice(["Admin", "Editor", "Viewer"])
            )
            db.add(user)
            db.flush() # Day du lieu de lay user_id
            
            # 2. Tao ngau nhien 2-5 tai lieu cho moi User
            num_docs = random.randint(2, 5)
            for i in range(num_docs):
                doc = Document(
                    id=uuid.uuid4(),
                    user_id=user.user_id,
                    file_name=f"Tai_lieu_{fake.word().capitalize()}.pdf",
                    file_path_url=f"/storage/docs/{fake.uuid4()}.pdf",
                    status=random.choice(["Pending", "Processing", "Completed"]),
                    version=random.randint(1, 5)
                )
                db.add(doc)
        
        db.commit()
        print(f"Da gieo thanh cong 50 User va hang tram tai lieu mau!")

    except Exception as e:
        print(f"Co loi xay ra: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_faker()
