from mongoengine import (EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         ComplexDateTimeField, BooleanField)

from models.id import WithID, WithIDEmbedded


class Commitments(WithIDEmbedded):
    amount = IntField()
    date = ComplexDateTimeField()

class Task(WithID):

    groupID = StringField()
    userID = StringField()
    description = StringField()
    beanReward = IntField()
    completeBy = ComplexDateTimeField()
    completed = BooleanField()
    commitments = ListField(EmbeddedDocumentField(Commitments))

