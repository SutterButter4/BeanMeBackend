import time

from mongoengine_goodjson import Document
from mongoengine import StringField, ObjectIdField, BooleanField, IntField

from models.group import Groups
from models.task import Tasks
from models.user import Users


class Notifications(Document):
    type = StringField(required=True)
    description = StringField(required=True, default="description")
    userOwnerId = ObjectIdField(required=True)
    userTopicId = ObjectIdField()
    groupId = ObjectIdField()
    taskId = ObjectIdField()
    date = IntField(default=int(1000*time.time()))
    viewed = BooleanField(default=False)
    beanCount = IntField()

    def generate_description(self):
        try:
            group = Groups.objects.get(id=self.groupId)
        except:
            group = None
        try:
            task = Tasks.objects.get(id=self.taskId)
        except:
            task = None
        try:
            user_topic = Users.objects.get(id=self.userTopicId)
        except:
            user_topic = None

        if self.type == "INVITE":
            d = f"You've been invited to join {group.name}"
        elif self.type == "TASK_CREATED":
            d = f"{user_topic.name} wants {task.beanReward} for {task.description}"
        elif self.type == "TASK_FULFILLED":
            d = f"{user_topic.name} has found {task.beanReward} beans for {task.description}"
        elif self.type == "OUT_OF_BEANS":
            d = f"{user_topic.name} in group {group.name} is out of beans"
        elif self.type == "INCOMING_TRANSFER":
            d = f"{user_topic.name} has given you {self.beanCount} beans in {group.name}"
        elif self.type == "USER_JOINED":
            d = f"{user_topic.name} has joined {group.name}"
        else:
            raise Exception("INVALID TYPE")

        self.description = str(d)

        pass

    def save(self, *args, **kwargs):
        # Overwrite Document save method to generate password hash prior to saving
        self.generate_description()
        super(Notifications, self).save(*args, **kwargs)