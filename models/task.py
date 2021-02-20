from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         BooleanField)
import mongoengine_goodjson as gj


class Commitments(gj.EmbeddedDocument):
    amount = IntField(db_field="amountPaid", required=True)
    date = IntField(db_field="date", required=True)

class Tasks(gj.Document):

    groupId = StringField(db_field="groupId", required=False)
    userId = StringField(db_field="userId", required=False)
    description = StringField(db_field="description", required=True)
    beanReward = IntField(db_field="beanReward", required=True)
    completeBy = IntField(db_field="completeBy", required=True)
    completed = BooleanField(db_field="completed", required=False)
    commitments = ListField(EmbeddedDocumentField(Commitments), db_field="commitments", required=False)

