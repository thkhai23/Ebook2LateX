from sqlalchemy.orm import Session
from app import models, schemas
from uuid import UUID

# --- User CRUD ---
def get_user(db: Session, user_id: UUID):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.username_email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # Lưu ý: Trong thực tế cần băm mật khẩu trước khi lưu
    db_user = models.User(
        username_email=user.username_email,
        password_hash=user.password, # Giả sử là hash
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Document CRUD ---
def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()

def create_user_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: UUID):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

# --- FormulaEntry CRUD ---
def create_formula_entry(db: Session, formula: schemas.FormulaEntryCreate):
    db_formula = models.FormulaEntry(**formula.model_dump())
    db.add(db_formula)
    db.commit()
    db.refresh(db_formula)
    return db_formula
