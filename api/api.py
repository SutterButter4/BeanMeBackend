# flask packages
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

class root(Resource):
    def get(self):
        return "OK", 200



#return the single user that called this method from the front end
class getUser(Resource):
    @jwt_required()
    def post(self):
        return current_user.to_json()





class getGroup(Resource):
    @jwt_required()
    def post(self):
        id = request.json.get('groupId')
        try:
            result = Groups.objects.get(id=id)
        except:
            return not_found_error("group not found")

        result = json.loads(result.to_json())
        for guser in result['users']:
            user = Users.objects.get(id=guser['userID'])
            guser.update({'name':user.name})
        return success()

    @jwt_required()
    def delete(self):
        try:
            id = request.json.get('groupId')
            group = Groups.objects.get(id=id)
            for users in group.users:
                if current_user.id == users.id:
                    group.delete()
                    return success()
            return unauthorized_error("Use Not In Group")
        except:
            return not_found_error("Group Not Found")


class makeGroup(Resource):
    @jwt_required()
    def post(self):
        groupName = request.json.get("name")

        gu = GroupUser(userId=str(current_user.id), beans=100)

        group = Groups(name=groupName,users=[gu])
        group.save()

        return success()

# a user inviting another user to a certain group
class getGroupTasks(Resource):
    @jwt_required()
    def post(self, id):
        result = Groups.objects.get(id=id).tasks
        if not result:
            return not_found_error("group not found")
        else:
            return result, success()


#a user inviting another to a group
class groupInvite(Resource):
    @jwt_required()
    def post(self):

        data = request.json()
        userID = data.userID
        groupID = data.groupID

        try:
            user = Users.objects.get(id=userID)
        except:
            return not_found_error("user not found")

        try:
            group = Groups.objects.get(id=groupID)
        except:
            return not_found_error("group not found")

        try:
            group.invitedUsers.objects.get(id=current_user.id)
        except:
            return unauthorized_error("user inviting is not in group")

        group.update(
            add_to_set__invitedUsers=user.id
        )

        return groupID


class acceptInvite(Resource):
    @jwt_required()
    def post(self):
        #if user is in list of invites, add to group and remove from invites
        data = request.get_json()
        try:
            group = Groups.objects.get(id=data.GroupId)
        except:
            return not_found_error("group not found")
        else:
            if current_user.id in group.invitedUsers:

                # remove user from this group's invites
                group.update(unset__invitedUsers=current_user.id)
                # add user to the group
                newUser = GroupUser(userId=current_user.id,beans=0)
                group.update(add_to_set__users=newUser)

            else:
                return not_found_error("invite not found")





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

        Groups \
            .objects(id=groupId) \
            .get\
            .objects(userID=current_user.id).get()
        try:
            a=1
        except:
            return not_found_error("user not in group")

        task = Tasks(groupId=groupId,
                     description=data.get("description"),
                     beanReward=data.get("beanReward"),
                     completeBy=data.get("completeBy"))

        task.save()

        return task.to_json()


class taskID(Resource):
    @jwt_required()
    def post(self):
        pass


class taskCommit(Resource):
    @jwt_required()
    def post(self):
        pass
