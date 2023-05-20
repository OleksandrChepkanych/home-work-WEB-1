from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.shemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name,
                second_name=body.second_name,
                email=body.email,
                phone=body.phone,
                birthday=body.birthday,
                description=body.description)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.second_name = body.second_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_some_info(some_info: str, db: Session) -> List[Contact]:
    response = []
    info_by_first_name = db.query(Contact).filter(
        Contact.first_name.like(f'%{some_info}%')).all()
    if info_by_first_name:
        for n in info_by_first_name:
            response.append(n)
    info_by_second_name = db.query(Contact).filter(
        Contact.second_name.like(f'%{some_info}%')).all()
    if info_by_second_name:
        for n in info_by_second_name:
            response.append(n)
    info_by_email = db.query(Contact).filter(
        Contact.email.like(f'%{some_info}%')).all()
    if info_by_email:
        for n in info_by_email:
            response.append(n)

    return response


async def get_birthday_per_week(days: int, db: Session) -> Contact:
    response = []
    all_contacts = db.query(Contact).all()
    for contact in all_contacts:
        if timedelta(0) <= ((contact.birthaday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(contact)

    return response
