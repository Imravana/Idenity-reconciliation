from sqlalchemy.orm import Session
from models import Contact, LinkPrecedence
from typing import List, Optional
from utils import build_consolidated_response

def consolidate_contacts(db, contacts):
    return build_consolidated_response(db, contacts)

def get_all_matching_contacts(db: Session, email: Optional[str], phone: Optional[str]) -> List[Contact]:
    """Return all contacts whose email or phone match the supplied values (ignoring soft‑deleted rows)."""
    query = db.query(Contact).filter(Contact.deletedAt.is_(None))
    if email and phone:
        return query.filter((Contact.email == email) | (Contact.phoneNumber == phone)).all()
    elif email:
        return query.filter(Contact.email == email).all()
    elif phone:
        return query.filter(Contact.phoneNumber == phone).all()
    return []


def create_contact(
    db: Session,
    email: Optional[str],
    phone: Optional[str],
    linked_id: Optional[int],
    link_precedence: str,
) -> Contact:
    """Insert a new contact row and return the persisted instance."""
    new_contact = Contact(
        email=email,
        phoneNumber=phone,
        linkedId=linked_id,
        linkPrecedence=link_precedence,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


def consolidate_contacts(db: Session, contacts: List[Contact]):
    """Merge a list of related contacts and return the consolidated response payload."""
    # The earliest (oldest) contact is always the primary
    primary_contact = min(contacts, key=lambda c: c.createdAt)
    primary_id = primary_contact.id

    # Demote any non‑primary contacts to secondary if they aren’t already
    for contact in contacts:
        if contact.id != primary_id and contact.linkPrecedence != LinkPrecedence.secondary:
            contact.linkPrecedence = LinkPrecedence.secondary
            contact.linkedId = primary_id
            db.add(contact)
    db.commit()

    # Fetch the full cluster (primary + all its secondaries)
    cluster = (
        db.query(Contact)
        .filter(((Contact.id == primary_id) | (Contact.linkedId == primary_id)) & (Contact.deletedAt.is_(None)))
        .all()
    )

    emails = list({c.email for c in cluster if c.email})
    phone_numbers = list({c.phoneNumber for c in cluster if c.phoneNumber})
    secondary_ids = [c.id for c in cluster if c.linkPrecedence == LinkPrecedence.secondary]

    return {
        "primaryContactId": primary_id,
        "emails": emails,
        "phoneNumbers": phone_numbers,
        "secondaryContactIds": secondary_ids,
    }
