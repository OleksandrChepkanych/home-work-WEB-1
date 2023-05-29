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
    contacts = await repository_contacts.get_contacts(skip, limit, db, current_contact)
    return contacts


@router.get("/find/{some_info}", response_model=List[ContactResponse])
async def find_contact_by_some_info(some_info: str, db: Session = Depends(get_db),
                                    current_contact: User = Depends(auth_service.get_current_contact)):
    contacts = await repository_contacts.get_contact_by_some_info(some_info, db, current_contact)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/birthday/{days}", response_model=List[ContactResponse])
async def find_birthday_per_week(days: int, db: Session = Depends(get_db),
                                 current_contact: User = Depends(auth_service.get_current_contact)):
    contacts = await repository_contacts.get_birthday_per_week(days, db, current_contact)
    if contacts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       current_contact: User = Depends(auth_service.get_current_contact)):
    contact = await repository_contacts.get_contact(contact_id, db, current_contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 1 requests per 1 minute',
             dependencies=[Depends(RateLimiter(times=15, seconds=60))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                      current_contact: User = Depends(auth_service.get_current_contact)):
    return await repository_contacts.create_contact(body, db, current_contact)


@router.put("/put/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_contact: User = Depends(auth_service.get_current_contact)):
    contact = await repository_contacts.update_contact(contact_id, body, db, current_contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/remove/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                         current_contact: User = Depends(auth_service.get_current_contact)):
    contact = await repository_contacts.remove_contact(contact_id, db, current_contact)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact