from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import shutil
import os

from database import SessionLocal, engine
from models import Base, Record

Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

templates = Jinja2Templates(directory="templates")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    db: Session = SessionLocal()
    records = db.query(Record).all()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "records": records
        }
    )


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )


@app.post("/upload")
async def upload_record(
    title: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...)
):

    filepath = f"{UPLOAD_DIR}/{file.filename}"

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db: Session = SessionLocal()

    new_record = Record(
        title=title,
        filename=file.filename,
        category=category
    )

    db.add(new_record)
    db.commit()

    return {
        "message": "Record uploaded successfully"
    }
