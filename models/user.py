# mongo-engine packages
from mongoengine import (EmbeddedDocumentField,
                         ListField,
                         StringField,
                         EmailField)

# flask packages
from flask_bcrypt import generate_password_hash, check_password_hash

from models.id import WithID

class Notification(object):
    description = StringField()
    groupID = StringField()
    taskID = StringField()


class Users(WithID):

    name = StringField()
    phone_num = StringField()
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True, min_length=6, regex=None)
    groups = ListField(EmbeddedDocumentField(StringField()))
    notifications =ListField(EmbeddedDocumentField(Notification))

    def generate_pw_hash(self):
        self.password_hash = generate_password_hash(self.password_hash).decode('utf-8')

    # Use documentation from BCrypt for password hashing
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)