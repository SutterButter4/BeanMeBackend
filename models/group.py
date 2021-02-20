from mongoengine import (Document,
                         EmbeddedDocument,
                         EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         ObjectIdField)
import mongoengine_goodjson as gj


class ScheduledTask(gj.EmbeddedDocument):

    taskId = ObjectIdField(db_field="taskID", required=True, primary_key=True)
    interval = IntField(db_field="timeInMS", required=True)

class GroupUser(gj.EmbeddedDocument):

    userId = ObjectIdField(db_field="userID", required=True)
    beans = IntField(db_field="numBeans", required=True)


class Groups(gj.Document):

    name = StringField(db_field="groupName", required=True)
    users = ListField(EmbeddedDocumentField(GroupUser), db_field="users", required=True)
    scheduledTasks = ListField(ObjectIdField(), db_field="scheduledTasks")
    invitedUsers = ListField(StringField(db_field="invitedUsers"))

