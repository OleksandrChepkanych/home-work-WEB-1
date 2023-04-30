from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    fullname = StringField(max_length=50, required=True)
    email = StringField()
    done = BooleanField(default=False)