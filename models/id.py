from mongoengine import Document, StringField, EmbeddedDocument

class WithID(Document):
    meta = {"allow_inheritance": True}
    id = StringField(db_field="groupName", required=True)

class WithIDEmbedded(EmbeddedDocument):
    meta = {"allow_inheritance": True}
    id = StringField(db_field="groupName", required=True)