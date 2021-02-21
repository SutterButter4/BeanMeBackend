import time

import mongoengine_goodjson as gj
from mongoengine import (EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         BooleanField,
                         ObjectIdField,
                         DateTimeField)


class Commitments(gj.EmbeddedDocument):
    amount = IntField(db_field="amountPaid", required=True)
    date = IntField(default=int(time.time()*1000), db_field="date", required=True)
    userId = ObjectIdField(db_field="userId", required=True)


class Tasks(gj.Document):

    groupId = ObjectIdField(db_field="groupId", required=True)
    assignee = ObjectIdField(db_field="assignee", required=True)
    creator = ObjectIdField(db_field="creator", required=True)
    description = StringField(db_field="description", required=True)
    beanReward = IntField(db_field="beanReward", required=True)
    completeBy = IntField(db_field="completeBy", required=True)
    completed = BooleanField(db_field="completed", required=False)
    fulfilled = BooleanField(db_field="fulfilled", default=False, required=False)
    commitments = ListField(EmbeddedDocumentField(Commitments), db_field="commitments", required=False)

