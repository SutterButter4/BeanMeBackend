# flask packages
import json
import time

from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from api.response import not_found_error, unauthorized_error, success, bad_request_error
# project resources
from models.group import Groups, ScheduledTask
from models.task import Tasks, Commitments
from models.user import Users
from models.notifications import Notifications


#add task to group
#TaskId, Interval(ms) --> group
class schedule_task(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        group_id = data.get('groupId')
        task_id = data.get('taskId')
        interval = data.get('interval')

        try:
            group = Groups.objects.get(id=group_id)
        except:
            return not_found_error("Group")
        if group.id not in current_user.groups:
            return unauthorized_error("User not in group")

        try:
            task = Tasks.objects.get(id=task_id)
        except:
            return not_found_error("Task not found")

        #ensure task not already scheudle
        groupScheduledOn = Groups.objects(scheduledTasks__taskId=task.id)
        if len(groupScheduledOn)==0:
            return bad_request_error("Task already scheduled")
        try:
            Groups.update(add_to_set__scheduledTasks=[ScheduledTask(task.id, interval)])
        except:
            return bad_request_error("Failed to save task schedule")


        return success()


class makeTask(Resource):
    @jwt_required()
    def post(self):

        data = request.get_json()

        groupId = data.get("groupId")       

        try:
            group = Groups.objects.get(id=groupId)
        except:
            return not_found_error("Group not found")


        if group.id not in current_user.groups:
            return unauthorized_error("User not in group")

        task = Tasks(groupId=group.id,
        description=data.get("description"),
        beanReward=int(data.get("beanReward")),
        completeBy=int(data.get("completeBy")),
        creator=current_user.id,
        assignee=current_user.id)

        try:
            task.save()
        except:
            return bad_request_error("Failed to save task")


        users_in_group = []

        for user in group.users:
            try:
                users_in_group.append(Users.objects.get(id=user.userId))
            except:
                pass

        notifs = []
        for user in users_in_group:
            notifs.append(Notifications(type="TASK_CREATED", taskId=task.id, userTopicId=current_user.id,groupId=group.id, userOwnerId=user.id))

        for notif in notifs:
            notif.save()
            Users.objects.get(id=notif.userOwnerId).update(push__notificationIds=notif.id)


        return success(task.to_json())



class taskId(Resource):
    @jwt_required()
    def post(self):
        id = request.json.get('taskId')
        try:
            task = Tasks.objects.get(id=id)
            taskGroup = Groups.objects.get(id=task.groupId)
        except:
            return bad_request_error("Invalid Task")

        if(taskGroup.id not in current_user.groups):
            return unauthorized_error("User is not in group of task")
        else:
            return success(task.to_json())

    @jwt_required()
    def delete(self):
        id = request.json.get('taskId')
        try:
            task = Tasks.objects.get(id=id)
            taskGroup = Groups.objects.get(id=task.groupId)
        except:
            return bad_request_error("Invalid Task")

        if(taskGroup.id not in current_user.groups):
            return unauthorized_error("User is not in group of task")

        taskGroup.update(pull__scheduledTasks__id=task.id)
        task.delete()
        return success()


class taskCommit(Resource):
    @jwt_required()
    def post(self):
        d = request.json
        taskId = d.get('taskId')
        amount = d.get('amount')
        try:
            task = Tasks.objects.get(id=taskId)
            group = Groups.objects.get(id=task.groupId)
        except:
            return bad_request_error("Invalid Task")
        if amount<=0:
            return bad_request_error("Invalid Amountp")
        user = None
        for gu in group.users:
            if gu.userId == current_user.id:
                user = gu
        if not user:
            return bad_request_error("User not in task group")
        if user.beans>=amount:
            c = Commitments(amount=amount, date=int(1000 * time.time()) ,userId=current_user.id)
            task.update(add_to_set__commitments=c)
            Groups.objects(id=group.id, users__userId=current_user.id).update(dec__users__S__beans=amount)
        else:
            return bad_request_error("Not Enough Beans")

        task = Tasks.objects.get(id=taskId)
        commited = 0
        for commit in task.commitments:
            commited += commit.amount

        if commited>=task.beanReward:
            task.update(set__fulfilled=True)
            users_in_group = []

            for user in group.users:
                try:
                    users_in_group.append(Users.objects.get(id=user.userId))
                except:
                    pass

            notifs =[]
            for user in users_in_group:
                notifs.append(Notifications(type="TASK_FULFILLED", userOwnerId=user.id, taskId=task.id, userTopicId=task.assignee))

            for notif in notifs:
                notif.save()
                Users.objects.get(id=notif.userOwnerId).update(push__notificationIds=notif.id)

        return success(task.to_json())

