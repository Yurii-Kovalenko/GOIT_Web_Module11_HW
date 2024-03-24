from typing import List

from sqlalchemy import func, extract, and_, or_

from sqlalchemy.orm import Session

from datetime import date, timedelta

from src.database.models import Contact
from src.schemas import ContactModel, ContactUpdate


async def get_contacts(
    skip: int,
    limit: int,
    first_name: str,
    last_name: str,
    email: str,
    birthdays: int,
    db: Session,
) -> List[Contact]:
    if len(f"{first_name}{last_name}{email}") == 0 and birthdays == 0:
        return db.query(Contact).offset(skip).limit(limit).all()
    elif len(first_name) > 0:
        return db.query(Contact).filter(Contact.first_name.startswith(first_name)).all()
    elif len(last_name) > 0:
        return db.query(Contact).filter(Contact.last_name.startswith(last_name)).all()
    elif len(email) > 0:
        return db.query(Contact).filter(Contact.email.startswith(email)).all()
    else:
        date_start = date.today()
        year_start = date_start.year
        date_finish = date.today() + timedelta(days=birthdays)
        year_finish = date_finish.year
        return (
            db.query(Contact)
            .filter(
                or_(
                    and_(
                        func.date(
                            func.concat(
                                year_start,
                                "-",
                                extract("month", Contact.date_of_birth),
                                "-",
                                extract("day", Contact.date_of_birth),
                            )
                        )
                        >= date_start,
                        func.date(
                            func.concat(
                                year_start,
                                "-",
                                extract("month", Contact.date_of_birth),
                                "-",
                                extract("day", Contact.date_of_birth),
                            )
                        )
                        <= date_finish,
                    ),
                    and_(
                        func.date(
                            func.concat(
                                year_finish,
                                "-",
                                extract("month", Contact.date_of_birth),
                                "-",
                                extract("day", Contact.date_of_birth),
                            )
                        )
                        >= date_start,
                        func.date(
                            func.concat(
                                year_finish,
                                "-",
                                extract("month", Contact.date_of_birth),
                                "-",
                                extract("day", Contact.date_of_birth),
                            )
                        )
                        <= date_finish,
                    ),
                )
            )
            .all()
        )


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone=body.phone,
        date_of_birth=body.date_of_birth,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(
    contact_id: int, body: ContactModel, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def update_date_of_birth_contact(
    contact_id: int, body: ContactUpdate, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact
