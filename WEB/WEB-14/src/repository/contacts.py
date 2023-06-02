from typing import List
from datetime import datetime, timedelta
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.shemas import ContactModel


async def get_contacts(skip: int, limit: int, db: Session, contact: User) -> List[Contact]:
    """
    The get_contacts function returns a list of contacts for the user.

    :param skip: int: Skip the first n contacts in the database
    :param limit: int: Limit the number of contacts returned
    :param db: Session: Access the database
    :param contact: User: Get the contacts of a specific user
    :return: A list of contacts
    :doc-author: Trelent
    """
    return db.query(Contact).filter(Contact.user_id == contact.id).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session, contact: User) -> Contact:
    """
    The get_contact function takes in a contact_id and returns the Contact object with that id.
    It also checks to make sure that the user is authorized to access this contact.

    :param contact_id: int: Identify the contact in the database
    :param db: Session: Pass the database session to the function
    :param contact: User: Ensure that the user is only able to get contacts from their own account
    :return: The first contact in the database that matches the id and user_id
    :doc-author: Trelent
    """
    return db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == contact.id)).first()


async def create_contact(body: ContactModel, db: Session, contact: User) -> Contact:
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            db (Session): The database session to use for creating the contact.

    :param body: ContactModel: Get the data from the request body
    :param db: Session: Access the database
    :param contact: User: Get the id of the user that is logged in
    :return: A contact object
    :doc-author: Trelent
    """
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
    """
    The update_contact function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified user.

    :param contact_id: int: Get the contact id from the url
    :param body: ContactModel: Get the contact details from the request body
    :param db: Session: Access the database
    :param contact: User: Get the user_id from the contact table
    :return: A contact object
    :doc-author: Trelent
    """
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
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.
            user (User): The user who is removing this contact.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Access the database
    :param contact: User: Get the user's id
    :return: A contact object or none
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == contact.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contact_by_some_info(some_info: str, db: Session, contact: User) -> List[Contact]:
    """
    The get_contact_by_some_info function takes a string and returns all contacts that have the string in their first name, second name or email.

    :param some_info: str: Search for contacts by first name, second name or email
    :param db: Session: Connect to the database
    :param contact: User: Get the user_id of the contact
    :return: A list of contacts that match the search criteria
    :doc-author: Trelent
    """
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
    """
    The get_birthday_per_week function takes in a number of days and returns all contacts whose birthday is within that
    number of days. It also takes in the database session and the user who's contacts are being searched.

    :param days: int: Specify the number of days in which we want to get the birthdays
    :param db: Session: Pass the database session to the function
    :param contact: User: Get the user id from the contact object
    :return: A list of contacts whose birthday is in the next 7 days
    :doc-author: Trelent
    """
    response = []
    all_contacts = db.query(Contact).filter(Contact.user_id == contact.id).all()
    for cont in all_contacts:
        if timedelta(0) <= ((cont.birthday.replace(year=int((datetime.now()).year))) - datetime.now().date()) <= timedelta(days):
            response.append(cont)
    return response