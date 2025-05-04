from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI()

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    name = Column(String)
    email = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

class InteractionInput(BaseModel):
    phone_number: str
    name: str
    email: str

@app.post("/add")
def add_interaction(data: InteractionInput):
    db = SessionLocal()
    interaction = Interaction(
        phone_number=data.phone_number,
        name=data.name,
        email=data.email
    )
    db.add(interaction)
    db.commit()
    db.close()
    return {"message": "Interação registrada com sucesso"}

@app.get("/count/{phone_number}")
def get_count(phone_number: str):
    db = SessionLocal()
    today = datetime.datetime.utcnow().date()
    tomorrow = today + datetime.timedelta(days=1)
    count = db.query(Interaction).filter(
        Interaction.phone_number == phone_number,
        Interaction.timestamp >= today,
        Interaction.timestamp < tomorrow
    ).count()
    db.close()
    return {"phone_number": phone_number, "count_today": count}
