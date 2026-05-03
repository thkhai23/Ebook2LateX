from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from decimal import Decimal

# --- User Schemas ---
class UserBase(BaseModel):
    username_email: str
    full_name: Optional[str] = None
    role: Optional[str] = "Editor"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: UUID
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Log Schemas ---
class LogBase(BaseModel):
    processing_time_ms: Optional[int] = None
    confidence_score: Optional[Decimal] = None
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    environment_info: Optional[Any] = None

class Log(LogBase):
    log_id: UUID
    formula_id: Optional[UUID] = None
    timestamp: datetime

    class Config:
        from_attributes = True

# --- FormulaEntry Schemas ---
class FormulaEntryBase(BaseModel):
    raw_image_path: Optional[str] = None
    latex_content: Optional[str] = None
    order_index: int

class FormulaEntryCreate(FormulaEntryBase):
    document_id: UUID

class FormulaEntry(FormulaEntryBase):
    id: UUID
    document_id: UUID
    created_at: datetime
    updated_at: datetime
    logs: List[Log] = []

    class Config:
        from_attributes = True

# --- Document Schemas ---
class DocumentBase(BaseModel):
    file_name: str
    file_path_url: str
    status: Optional[str] = "Pending"

class DocumentCreate(DocumentBase):
    user_id: Optional[UUID] = None

class Document(DocumentBase):
    id: UUID
    user_id: Optional[UUID] = None
    upload_date: datetime
    formulas: List[FormulaEntry] = []

    class Config:
        from_attributes = True
