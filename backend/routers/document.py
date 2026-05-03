from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import crud, schemas, database

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.get("/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit)
    return documents

@router.post("/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(database.get_db)):
    return crud.create_user_document(db=db, document=document)

@router.get("/{document_id}", response_model=schemas.Document)
def read_document(document_id: UUID, db: Session = Depends(database.get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document
