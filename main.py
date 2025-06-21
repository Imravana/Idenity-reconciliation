from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify_contact(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    email = payload.email
    phone = payload.phoneNumber

    if not email and not phone:
        raise HTTPException(status_code=400, detail="At least email or phoneNumber must be provided.")

    matched_contacts = crud.get_all_matching_contacts(db, email, phone)

    if not matched_contacts:
        # No match: create a primary contact
        new_contact = crud.create_contact(db, email, phone, linked_id=None, link_precedence="primary")
        return {"contact": {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }}

    # Found existing: create new secondary contact (if not duplicate)
    exists = any(c.email == email and c.phoneNumber == phone for c in matched_contacts)
    if not exists:
        primary_id = min(matched_contacts, key=lambda c: c.createdAt).id
        crud.create_contact(db, email, phone, linked_id=primary_id, link_precedence="secondary")

    # Merge and return consolidated info
    return {"contact": crud.consolidate_contacts(db, crud.get_all_matching_contacts(db, email, phone))}