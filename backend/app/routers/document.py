import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app import crud, schemas, database
from app.ai_pipeline import process_pdf_to_latex

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

@router.post("/upload", response_model=schemas.Document)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # 1. Save file (mock)
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Create Document record
    doc_create = schemas.DocumentCreate(
        file_name=file.filename,
        file_path_url=file_path,
        status="Processing"
    )
    db_document = crud.create_user_document(db, doc_create)
    
    # 3. Process with AI Pipeline
    try:
        formulas = process_pdf_to_latex(file_path)
        
        # 4. Save Formulas and Logs
        for f_data in formulas:
            formula_create = schemas.FormulaEntryCreate(
                document_id=db_document.id,
                latex_content=f_data["latex_content"],
                order_index=f_data["order_index"]
            )
            db_formula = crud.create_formula_entry(db, formula_create)
            
            # Log the processing for each formula
            log_data = schemas.LogBase(
                processing_time_ms=500, # Mock
                confidence_score=f_data["confidence_score"],
                environment_info={"model": "mock-ai-v1"}
            )
            crud.create_log(db, log_data, formula_id=db_formula.id)
            
        # Update status to Completed
        db_document.status = "Completed"
        db.commit()
        db.refresh(db_document)
        
    except Exception as e:
        db_document.status = "Error"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))
    
    return db_document

@router.get("/{document_id}", response_model=schemas.Document)
def read_document(document_id: UUID, db: Session = Depends(database.get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.put("/formula/{formula_id}", response_model=schemas.FormulaEntry)
def update_formula(formula_id: UUID, formula_update: schemas.FormulaEntryBase, db: Session = Depends(database.get_db)):
    db_formula = crud.update_formula_entry(db, formula_id=formula_id, latex_content=formula_update.latex_content)
    if db_formula is None:
        raise HTTPException(status_code=404, detail="Formula not found")
    return db_formula
