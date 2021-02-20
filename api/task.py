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


from api.response import not_found_error, unauthorized_error, success,bad_request_error
import datetime
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





class makeTask(Resource):
    @jwt_required()
    def post(self):

        data = request.get_json()

        groupId = data.get("groupId")       

        try:
            group = Groups.objects.get(id=groupId)
        except:
            return not_found_error("Group not found")

        if group.id in current_user.groups:
            task = Tasks(groupId=group.id,
            description=data.get("description"),
            beanReward=int(data.get("beanReward")),
            completeBy=datetime.utcnow,
            creator=current_user.id,
            assignee=current_user.id)
            
            try:
                task.save()
                #add scheduled task to group
                st = ScheduledTask(taskId=task.id)
                group.update(add_to_set__scheduledTasks=st)
            
                return success(task.to_json())
            except Exception as e:
                return bad_request_error(e)#"Failed to save task")

        else:
            return unauthorized_error("User not in group")
        

        

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
            return task.to_json()

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
        else:
            taskGroup.update(pull__scheduledTasks__id=task.id)
            task.delete()
            return success()


class taskCommit(Resource):
    @jwt_required()
    def post(self):
        d = request.json
        taskId = d.get('taskId')
        amount = d.get('Amount')
        try:
            task = Tasks.objects.get(id=taskId)
            taskGroup = Groups.objects.get(id=task.groupId)
        except:
            return bad_request_error("Invalid Task")
        
        for user in taskGroup.users:
            if current_user.id == user.id:
                if(user.beans>=amount):
                    c = Commitments(amount=amount,date=datatime.now(),userId=user.id)
                    task.update(add_to_set__commitments=c)
                    user.update(dec__beans=amount)
                    return task.to_json(), success()
                else:
                    return bad_request_error("Not Enough Beans")
        
        return bad_request_error("User Not In Task Group")
