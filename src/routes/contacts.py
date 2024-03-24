from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts


router = APIRouter(prefix="/contacts", tags=["contacts"])

contact_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 20,
    first_name: str = "",
    last_name: str = "",
    email: str = "",
    birthdays: int = 0,
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.get_contacts(
        skip, limit, first_name, last_name, email, birthdays, db
    )
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise contact_not_found
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise contact_not_found
    return contact


@router.patch("/{contact_id}", response_model=ContactResponse)
async def update_date_of_birth_contact(
    body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_date_of_birth_contact(
        contact_id, body, db
    )
    if contact is None:
        raise contact_not_found
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise contact_not_found
    return contact
