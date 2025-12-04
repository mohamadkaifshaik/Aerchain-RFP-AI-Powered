from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from .db import engine, init_db
from .models import RFP, Vendor, Proposal, RFPCreate, VendorCreate, IngestProposal
from .email_service import send_email
from uuid import UUID

app = FastAPI(title="RFP Mail Demo")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/api/rfps", response_model=RFP)
def create_rfp(payload: RFPCreate):
    r = RFP(title=payload.title, description=payload.description, budget_cents=payload.budget_cents, items=payload.items)
    with Session(engine) as session:
        session.add(r)
        session.commit()
        session.refresh(r)
        return r

@app.get("/api/rfps")
def list_rfps():
    with Session(engine) as session:
        return session.exec(select(RFP)).all()

@app.post("/api/vendors", response_model=Vendor)
def create_vendor(payload: VendorCreate):
    v = Vendor(name=payload.name, primary_email=payload.primary_email)
    with Session(engine) as session:
        session.add(v)
        session.commit()
        session.refresh(v)
        return v

@app.get("/api/vendors")
def list_vendors():
    with Session(engine) as session:
        return session.exec(select(Vendor)).all()

@app.post("/api/rfps/{rfp_id}/send")
def send_rfp(rfp_id: UUID, vendor_ids: list[UUID]):
    with Session(engine) as session:
        rfp = session.get(RFP, rfp_id)
        if not rfp:
            raise HTTPException(status_code=404, detail="RFP not found")
        vendors = [session.get(Vendor, v) for v in vendor_ids]
        sent = []
        for vendor in vendors:
            if vendor:
                subject = f"RFP: {rfp.title}"
                body = f"Hello {vendor.name},\n\nPlease provide a proposal for the following RFP:\n\nTitle: {rfp.title}\nDescription:\n{rfp.description}\n\nRFP id: {rfp.id}\n\nThanks"
                ok, err = send_email(vendor.primary_email, subject, body)
                sent.append({"vendor": vendor.primary_email, "ok": ok, "error": err})
        return {"sent": sent}

@app.post("/api/proposals/ingest", response_model=Proposal)
def ingest_proposal(payload: IngestProposal):
    # store raw proposal into DB
    p = Proposal(rfp_id=payload.rfp_id, vendor_email=payload.vendor_email, raw_email_text=payload.raw_text)
    with Session(engine) as session:
        session.add(p)
        session.commit()
        session.refresh(p)
        return p
