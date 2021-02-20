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





