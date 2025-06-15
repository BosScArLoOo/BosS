from fastapi import APIRouter, Form
from database import SessionLocal, ChatMessage

router = APIRouter()

@router.post("/send_message/")
def send_message(sender: str = Form(...), message: str = Form(...)):
    db = SessionLocal()
    msg = ChatMessage(sender=sender, message=message)
    db.add(msg)
    db.commit()
    db.close()
    return {"message": "Message sent."}

@router.get("/get_messages/")
def get_messages():
    db = SessionLocal()
    messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.asc()).all()
    db.close()
    return messages
