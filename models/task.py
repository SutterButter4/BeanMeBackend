from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         ComplexDateTimeField, BooleanField)


class Commitments(EmbeddedDocument):
    amount = IntField()
    date = ComplexDateTimeField()

class Tasks(Document):

    groupID = StringField()
    userID = StringField()
    description = StringField()
    beanReward = IntField()
    completeBy = ComplexDateTimeField()
    completed = BooleanField()
    commitments = ListField(EmbeddedDocumentField(Commitments))

