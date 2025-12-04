from typing import Optional, List, Dict
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, EmailStr

class RFP(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    budget_cents: Optional[int] = None
    items: Optional[Dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Vendor(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    primary_email: str

class Proposal(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    rfp_id: UUID
    vendor_email: Optional[str] = None
    raw_email_text: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Pydantic models for requests
class RFPCreate(BaseModel):
    title: str
    description: Optional[str] = None
    budget_cents: Optional[int] = None
    items: Optional[Dict] = None

class VendorCreate(BaseModel):
    name: str
    primary_email: EmailStr

class IngestProposal(BaseModel):
    rfp_id: UUID
    vendor_email: EmailStr
    raw_text: str
