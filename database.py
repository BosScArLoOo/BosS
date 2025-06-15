from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./student_admin.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc)

class PDF(Base):
    __tablename__ = 'pdfs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    filename = Column(String)

class Announcement(Base):
    __tablename__ = 'announcements'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    timestamp = Column(DateTime, default=utc_now)

class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=utc_now)

Base.metadata.create_all(bind=engine)
