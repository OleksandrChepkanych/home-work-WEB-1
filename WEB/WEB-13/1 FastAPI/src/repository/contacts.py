from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.shemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, contact: User) -> List[Contact]:
    return db.query(Contact).filter(Contact.user_id == contact.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session, contact: User) -> Contact:
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == contact.id)).first()


async def create_contact(body: ContactModel, db: Session, contact: User) -> Contact:
    contact = Contact(first_name=body.first_name,
                      second_name=body.second_name,
                      email=body.email,
                      phone=body.phone,
                      birthday=body.birthday,
                      description=body.description,
                      user_id=contact.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session, contact: User) -> Contact | None:
    contact = db.query(Contact).filter(
        and_(Contact.id == contact_id, Contact.user_id == contact.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.second_name = body.second_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.description = body.description
        contact.user_id = contact.id
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, contact: User) -> Contact | None:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == contact.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_some_info(some_info: str, db: Session, contact: User) -> List[Contact]:
    response = []
    info_by_first_name = db.query(Contact).filter(
        and_(Contact.first_name.like(f'%{some_info}%'), Contact.user_id == contact.id)).all()
    if info_by_first_name:
        for n in info_by_first_name:
            response.append(n)
    info_by_second_name = db.query(Contact).filter(
        and_(Contact.second_name.like(f'%{some_info}%'), Contact.user_id == contact.id)).all()
    if info_by_second_name:
        for n in info_by_second_name:
            response.append(n)
    info_by_email = db.query(Contact).filter(
        and_(Contact.email.like(f'%{some_info}%'), Contact.user_id == contact.id)).all()
    if info_by_email:
        for n in info_by_email:
            response.append(n)
    return response


async def get_birthday_per_week(days: int, db: Session, contact: User) -> Contact:
    response = []
    all_contacts = db.query(Contact).filter(Contact.user_id == contact.id).all()
    for cont in all_contacts:
        if timedelta(0) <= ((cont.birthday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(cont)
    return response