import mongoengine_goodjson as gj

from mongoengine import (EmbeddedDocumentField,
                         ListField,
                         StringField,
                         IntField,
                         ObjectIdField)

from models.user import Users


class ScheduledTask(gj.EmbeddedDocument):

    taskId = ObjectIdField(db_field="taskId", required=True)
    interval = IntField(db_field="timeInMS", required=False)

class GroupUser(gj.EmbeddedDocument):

    userId = ObjectIdField(db_field="userId", required=True)
    beans = IntField(db_field="numBeans", required=True)


class Groups(gj.Document):

    name = StringField(db_field="groupName", required=True)
    users = ListField(EmbeddedDocumentField(GroupUser), db_field="users", required=True)
    scheduledTasks = ListField(ScheduledTask(), db_field="scheduledTasks")

    # def validate(self):
    #     badUsers = []
    #     for user in self.users:
    #         if len(Users.objects(id=user.userId)==0):
    #             badUsers.append(user)
    #     for user in badUsers:
    #         self.update(pull__users=user)
    #     super(Groups, self).validate()
