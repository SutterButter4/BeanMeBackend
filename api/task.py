# flask packages
import json

import jwt
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from bson.objectid import ObjectId

# project resources
from models.user import Users
from models.group import Groups, GroupUser, ScheduledTask
from models.task import Tasks


from api.errors import not_found_error, unauthorized_error, success

import json

#add task to group
#TaskId, Interval(ms) --> group
class schedule_task(Resource):
    @jwt_required()
    def post(self):

        data = request.get_json()
        group_id = data.get('group_id')
        task_id = data.get('task_id')
        interval = data.get('interval')

        try:
            group = Groups.objects.get(id=group_id)
        except:
            return "GROUP NOT FOUND", 404

        try:
            task = Tasks.objects.get(id=task_id)
        except:
            return "TASK NOT FOUND", 404

        #ensure task not already scheudled

        groupScheduledOn = Groups.objects.get(scheduledTasks__id=task_id).one_or_none()

        if not groupScheduledOn:
            Groups.update(add_to_set__scheduledTasks=[ScheduledTask(task_id, interval)])
            return success()
        else:
            return "TASK ALREADY SCHEDULED", 400



class transfer(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            group = Groups.objects.get(id=data.get('groupId'))
        except:
            return "GROUP NOT FOUND", 404


        for user in group.users:
            if(user.id == current_user.id):
                guser = user
            if(user.id == data.get('TargetUser').id):
                tuser = user
        beans = data.get('Amount')
        if(guser and tuser):
            if guser.beans>=beans:
                guser.update(dec__beans=beans)
                tuser.update(inc__beans=beans)
                return "OK", 201
            else:
                return "INSUFFICIENT BALANCE", 400
        else:
            return "Cant find users", 404

class makeTask(Resource):
    @jwt_required()
    def post(self):

        data = request.get_json()

        groupId = data.get("groupId")

        groupThisId = Groups.objects.get(id=groupId)
        gu = 0
        for groupUser in groupThisId.users:
            if groupUser.userId == current_user.id:
                gu = groupUser
                break

        if gu == 0:
            return not_found_error("user not in group")

        try:
            A=1
        except:
            return not_found_error("user not in group")

        task = Tasks(groupId=groupId,
                     description=data.get("description"),
                     beanReward=data.get("beanReward"),
                     completeBy=data.get("completeBy"))

        task.save()

        return json.loads(task.to_json())


class taskID(Resource):
    @jwt_required()
    def delete(self):
        id = request.json.get('taskId')
        task = Tasks.objects.get(id=id)
        taskGroup = Groups.objects.get(id=task.groupId)

        for userGuide in taskGroup.users:
            if userGuide.userId == current_user.id:
                return task

        return unauthorized_error("user is not in group of task")


class taskCommit(Resource):
    @jwt_required()
    def post(self):
        pass
