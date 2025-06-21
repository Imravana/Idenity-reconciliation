from models import Contact, LinkPrecedence
from sqlalchemy.orm import Session
from typing import List

def build_consolidated_response(db: Session, contacts: List[Contact]) -> dict:
    primary_contact = min(contacts, key=lambda c: c.createdAt)
    primary_id = primary_contact.id

    for c in contacts:
        if c.id != primary_id and c.linkPrecedence != LinkPrecedence.secondary:
            c.linkPrecedence = LinkPrecedence.secondary
            c.linkedId = primary_id
            db.add(c)
    db.commit()

    all_contacts = db.query(Contact).filter(
        (Contact.id == primary_id) | (Contact.linkedId == primary_id)
    ).filter(Contact.deletedAt.is_(None)).all()

    emails = list({c.email for c in all_contacts if c.email})
    phones = list({c.phoneNumber for c in all_contacts if c.phoneNumber})
    secondary_ids = [c.id for c in all_contacts if c.linkPrecedence == LinkPrecedence.secondary]

    return {
        "primaryContactId": primary_id,
        "emails": emails,
        "phoneNumbers": phones,
        "secondaryContactIds": secondary_ids
    }
