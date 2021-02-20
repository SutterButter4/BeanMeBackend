from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         BooleanField,
                         ObjectIdField,
                         DateTimeField)
import mongoengine_goodjson as gj
import datetime

class Commitments(gj.EmbeddedDocument):
    amount = IntField(db_field="amountPaid", required=True)
    date = DateTimeField(default=datetime.datetime.utcnow, db_field="date", required=True)
    userId = ObjectIdField(db_field="userId", required=True)


class Tasks(gj.Document):

    groupId = ObjectIdField(db_field="groupId", required=True)
    assignee = ObjectIdField(db_field="assignee", required=True)
    creator = ObjectIdField(db_field="creator", required=True)
    description = StringField(db_field="description", required=True)
    beanReward = IntField(db_field="beanReward", required=True)
    completeBy = DateTimeField(db_field="completeBy", required=True)
    completed = BooleanField(db_field="completed", required=False)
    commitments = ListField(EmbeddedDocumentField(Commitments), db_field="commitments", required=False)

