from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas import UserModel

from libgravatar import Gravatar


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_contact = User(**body.dict(), avatar=avatar)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_token(contact: User, token: str | None, db: Session) -> None:
    contact.refresh_token = token
    db.commit()