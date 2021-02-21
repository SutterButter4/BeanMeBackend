# mongo-engine packages
import re

from mongoengine_goodjson import Document
# flask packages
from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import (ListField,
                         StringField,
                         ObjectIdField)


class PhoneField(StringField):
    """
    Custom StringField to verify Phone numbers.
    # Modification of http://regexlib.com/REDetails.aspx?regexp_id=61
    #
    # US Phone number that accept a dot, a space, a dash, a forward slash, between the numbers.
    # Will Accept a 1 or 0 in front. Area Code not necessary
    """
    REGEX = re.compile(r"((\(\d{3}\)?)|(\d{3}))([-\s./]?)(\d{3})([-\s./]?)(\d{4})")

    def validate(self, value):
        # Overwrite StringField validate method to include regex phone number check.
        if not PhoneField.REGEX.match(string=value):
            self.error(f"ERROR: `{value}` Is An Invalid Phone Number.")
        super(PhoneField, self).validate(value=value)

class Users(Document):

    phone = PhoneField(db_field="phone", required=True, unique=True)
    name = StringField(required=False,default="John Doe")
    password = StringField(db_field="password", required=True, min_length=6, regex=None)
    groups = ListField(ObjectIdField(), db_field="groups")
    notificationIds = ListField(ObjectIdField(), db_field="notificationIds")
    invites = ListField(ObjectIdField(),db_field="invites")

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
