from sqlalchemy.orm import Session
from unittest.mock import MagicMock
import unittest

from src.database.models import Contact, User
from src.shemas import ContactModel
from src.repository.contacts import(get_contacts, get_contact, create_contact, update_contact, remove_contact,)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, db=self.session, contact=self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, db=self.session, contact=self.user)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, db=self.session, contact=self.user)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(first_name="Petya",
                            second_name="Pupkin",
                            email="petyapupkin@gmail.com",
                            phone="0509999999",
                            birthday="2000-01-01",
                            description="Test description")
        result = await create_contact(body=body, db=self.session, contact=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.second_name, body.second_name)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, db=self.session, contact=self.user)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, db=self.session, contact=self.user)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        contact = Contact(first_name="Petya", second_name="Pupkin", birthday="2000-01-01",
                            email="petyapupkin@gmail.com", phone="0509999999")
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact, db=self.session, contact=self.user)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        contact = Contact(first_name="Petya", second_name="Pupkin",
                          birthday="1999-01-01")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=contact, db=self.session, contact=self.user)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()