from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, PDF, Announcement
from chat import router as chat_router
import os
import uvicorn

app = FastAPI()

UPLOAD_DIR = "./uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Chat router must be included before app runs
app.include_router(chat_router)

# الصفحة الرئيسية
@app.get("/")
async def read_root():
    return {"message": "أهلاً بك في تطبيق إدارة الطلاب!"}

# Upload PDF
@app.post("/upload_pdf/")
def upload_pdf(title: str = Form(...), file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        while True:
            chunk = file.file.read(1024 * 1024)  # Read in 1MB chunks
            if not chunk:
                break
            buffer.write(chunk)

    db = SessionLocal()
    pdf = PDF(title=title, filename=file.filename)
    db.add(pdf)
    db.commit()
    return {"message": "PDF uploaded successfully."}

@app.get("/list_pdfs/")
def list_pdfs():
    db = SessionLocal()
    return db.query(PDF).all()

@app.get("/download_pdf/{pdf_id}")
def download_pdf(pdf_id: int):
    db = SessionLocal()
    pdf = db.query(PDF).filter(PDF.id == pdf_id).first()
    path = os.path.join(UPLOAD_DIR, pdf.filename)
    return FileResponse(path)

# Announcements
@app.post("/add_announcement/")
def add_announcement(content: str = Form(...)):
    db = SessionLocal()
    ann = Announcement(content=content)
    db.add(ann)
    db.commit()
    return {"message": "Announcement posted."}

@app.get("/announcements/")
def get_announcements():
    db = SessionLocal()
    return db.query(Announcement).order_by(Announcement.timestamp.desc()).all()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
