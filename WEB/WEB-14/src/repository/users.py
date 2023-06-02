from sqlalchemy.orm import Session

from src.database.models import User
from src.shemas import UserModel

from libgravatar import Gravatar


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists,
    it will return None.

    :param email: str: Pass in the email address of a user
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object to be created.
            db (Session): The SQLAlchemy session object used for querying the database.

    :param body: UserModel: Get the data from the request body
    :param db: Session: Access the database
    :return: The newly created user
    :doc-author: Trelent
    """
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
    """
    The update_token function updates the refresh token for a given user.

    :param contact: User: Identify the user in the database
    :param token: str | None: Update the refresh token of a user
    :param db: Session: Pass the database session to the function
    :return: None
    :doc-author: Trelent
    """
    contact.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Specify the email of the user to be confirmed
    :param db: Session: Pass the database session into the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that is being passed into the function
    :param db: Session: Pass the database session to the function
    :return: The updated user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user