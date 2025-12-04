from sqlmodel import create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rfp_mail_demo.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    from .models import RFP, Vendor, Proposal
    SQLModel.metadata.create_all(engine)
