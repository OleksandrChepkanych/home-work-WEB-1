from sqlalchemy.orm import Session
from unittest.mock import MagicMock
import unittest

from src.database.models import User
from src.shemas import UserModel
from src.repository.users import(get_user_by_email, create_user, update_token, confirmed_email, update_avatar,)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_user_by_email_found(self):
        user = self.user
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email("", db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email("petyapupkin", self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username="Petya Pupkin",
                         email="petyapupkin@gmail.com", password="password")
        result = await create_user(body, self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token(self):
        user = User()
        token = None
        await update_token(contact=user, token=token, db=self.session)
        self.assertEqual(user.refresh_token, token)

    async def test_confirmed_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        await confirmed_email("", self.session)
        self.assertEqual(user.confirmed, True)

    async def test_update_avatar(self):
        user = User()
        url = "https://gravatar.com"
        self.session.query().filter().first.return_value = user
        result = await update_avatar("", url, self.session)
        self.assertEqual(result.avatar, url)


if __name__ == '__main__':
    unittest.main()