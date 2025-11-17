from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Any, Dict

from database import create_document, get_documents, db
from schemas import ContactMessage

app = FastAPI(title="Portfolio API", version="1.0.0")

# CORS for local dev and hosted preview
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict[str, str]:
    return {"status": "ok", "service": "portfolio-backend"}


@app.get("/test")
def test_db() -> Dict[str, Any]:
    try:
        # Quick ping by listing collections
        collections = db.list_collection_names() if db else []
        return {"database_connected": db is not None, "collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/contact")
def create_contact(message: ContactMessage) -> Dict[str, str]:
    try:
        # Store message in the collection named after the schema (lowercase)
        collection_name = ContactMessage.__name__.lower()
        create_document(collection_name, message)
        return {"message": "Contact message received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
