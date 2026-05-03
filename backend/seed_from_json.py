import json
import uuid
from database import SessionLocal
from app.models import FormulaEntry, Document

def seed_from_json():
    db = SessionLocal()
    try:
        # Lay mot tai lieu bat ky de gan cac cong thuc vao
        doc = db.query(Document).first()
        if not doc:
            print("Loi: Khong tim thay tai lieu nao trong DB. Hay chay seed_faker.py truoc!")
            return

        # Doc du lieu tu file JSON
        with open('data.json', 'r', encoding='utf-8') as f:
            formula_data = json.load(f)
            
        print(f"Dang nap {len(formula_data)} cong thuc tu JSON vao tai lieu: {doc.file_name}")
        
        for item in formula_data:
            new_formula = FormulaEntry(
                id=uuid.uuid4(),
                document_id=doc.id,
                latex_content=item['latex'],
                order_index=item['order']
            )
            db.add(new_formula)
        
        db.commit()
        print("Da nap du lieu tu JSON thanh cong!")

    except Exception as e:
        print(f"Co loi xay ra: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_from_json()
