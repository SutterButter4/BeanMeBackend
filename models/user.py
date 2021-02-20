# mongo-engine packages
from mongoengine import (Document,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         EmailField,EmbeddedDocument)

# flask packages
from flask_bcrypt import generate_password_hash, check_password_hash

class Notification(EmbeddedDocument):
    description = StringField()
    groupID = StringField()
    taskID = StringField()


class Users(Document):

    name = StringField(db_field="name", required=True, unique=True)
    phone = StringField(db_field="phone", required=True, unique=True)
    email = EmailField
    password = StringField(db_field="password", required=True, min_length=6, regex=None)
    groups = ListField(StringField())
    notifications = ListField(EmbeddedDocumentField(Notification))

    def generate_pw_hash(self):
        self.password = generate_password_hash(self.password).decode('utf-8')

    # Use documentation from BCrypt for password hashing
    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    # Use documentation from BCrypt for password hashing
    check_pw_hash.__doc__ = check_password_hash.__doc__

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_pw_hash()
        super(Users, self).save(*args, **kwargs)