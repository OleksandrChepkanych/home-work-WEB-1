from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.shemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/all", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                     current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The read_contacts function returns a list of contacts.

    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned in a single request
    :param db: Session: Get the database session
    :param current_contact: User: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_contact)
    return contacts


@router.get("/find/{some_info}", response_model=List[ContactResponse])
async def find_contact_by_some_info(some_info: str, db: Session = Depends(get_db),
                                    current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The find_contact_by_some_info function is used to find a contact by some information.
        The function takes in the following parameters:
            - some_info (str): A string containing the information that will be used to search for a contact.
            - db (Session, optional): An SQLAlchemy Session instance that can be used for database operations. Defaults to Depends(get_db).
            - current_contact (User, optional): A User object representing the currently logged-in user making this request. Defaults to Depends(auth_service.get_current_contact).

    :param some_info: str: Specify the search criteria
    :param db: Session: Get the database session
    :param current_contact: User: Get the current contact
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contact_by_some_info(some_info, db, current_contact)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/birthday/{days}", response_model=List[ContactResponse])
async def find_birthday_per_week(days: int, db: Session = Depends(get_db),
                                 current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The find_birthday_per_week function returns a list of contacts that have their birthday in the next 7 days.
        The function takes an integer as input, which is the number of days to look ahead for birthdays.
        It also takes a database session and current_contact as inputs.

    :param days: int: Specify the number of days in a week
    :param db: Session: Get the database session
    :param current_contact: User: Get the current user
    :return: A list of contacts that have a birthday in the next 7 days
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_birthday_per_week(days, db, current_contact)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The read_contact function is a GET endpoint that returns the contact with the given ID.
    It requires authentication and authorization, as it depends on auth_service.get_current_contact().
    If no contact exists with the given ID, it raises an HTTPException.

    :param contact_id: int: Specify the contact id to be read
    :param db: Session: Pass the database session to the function
    :param current_contact: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact(contact_id, db, current_contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 1 requests per 1 minute',
             dependencies=[Depends(RateLimiter(times=15, seconds=60))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                      current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Get the contact information from the request body
    :param db: Session: Pass the database session to the repository layer
    :param current_contact: User: Get the current contact
    :return: The created contact
    :doc-author: Trelent
    """
    return await repository_contacts.create_contact(body, db, current_contact)


@router.put("/put/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The update_contact function updates a contact in the database.
        The function takes three arguments:
            - body: A ContactModel object containing the new data for the contact.
            - contact_id: An integer representing the ID of an existing contact to be updated.
            - db (optional): A Session object that can be used to access and modify data in a database, if not provided, one will be created automatically by dependency injection using get_db().

    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Specify the id of the contact to be updated
    :param db: Session: Pass the database session to the repository layer
    :param current_contact: User: Get the current contact
    :return: The contact that was updated
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(contact_id, body, db, current_contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/remove/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_contact: User = Depends(auth_service.get_current_contact)):
    """
    The remove_contact function removes a contact from the database.

    :param contact_id: int: Specify the contact to be removed
    :param db: Session: Pass the database session to the repository function
    :param current_contact: User: Get the current user
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db, current_contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact