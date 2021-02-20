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


from api.response import bad_request_error,not_found_error, unauthorized_error, success

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
            user = Users.objects.get(id=guser['userId'])
            guser.update({'name':user.name})
        return success(result)

    @jwt_required()
    def delete(self):
        try:
            id = request.json.get('groupId')
            group = Groups.objects.get(id=id)
            
            if group.id in current_user.groups:
                group.delete()
                return success()
            return unauthorized_error("Use Not In Group")
        except:
            return not_found_error("Group Not Found")


class makeGroup(Resource):
    @jwt_required()
    def post(self):
        groupName = request.json.get("name")

        gu = GroupUser(userId=current_user.id, beans=10)

        group = Groups(name=groupName,users=[gu])
        try:
            group.save()
        except:
            return bad_request_error("Could not save group")
        try:
            Users.objects(id=current_user.id).update_one(push__groups=group.id)
            return success("Successfully created group and added user")
        except Exception as e:
            group.delete()
            return bad_request_error(e.to_json())

#get all tasks in a group
class getGroupTasks(Resource):
    @jwt_required()
    def post(self):
        id = request.json.get('groupId')
        try:
            group = Groups.objects.get(id=id)
            if group.id in current_user.groups:
                return success(group.scheduledTasks)
            else:
                return unauthorized_error("User not in group")
        except Exception as e:
            return not_found_error("Group not found")


#a user inviting another to a group
class groupInvite(Resource):
    @jwt_required()
    def post(self):

        data = request.json
        phone = data.get('phone')
        groupID = data.get('groupId')

        try:
            user = Users.objects.get(phone=phone)
        except:
            return not_found_error("User not found")

        try:
            group = Groups.objects.get(id=groupID)
        except:
            return not_found_error("Group not found")

        if group.id not in current_user.groups:
            return unauthorized_error("User inviting is not in group")
        try:
            user.update(add_to_set__invites=group.id)
            return success("Successfully invited user")
        except Exception as e:
            return bad_request_error("Could not invite user")


class acceptInvite(Resource):
    @jwt_required()
    def post(self):
        #get group
        try:
            group = Groups.objects.get(id=request.json.get('groupId'))
        except:
            return not_found_error("Group not found")
        else:
            if group.id in current_user.invites:
                # remove invite from user profile
                current_user.update(pull__invites=group.id)
                # add user to the group
                newUser = GroupUser(userId=current_user.id,beans=10)
                group.update(add_to_set__users=newUser)
                return success("Successfully added to group")
            else:
                return not_found_error("No invite to this group")


class transfer(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            group = Groups.objects.get(id=data.get('groupId'))
        except:
            return not_found_error("Group not found")
        try:
            target = Users.objects.get(id=data.get('targetUser'))
        except:
            return not_found_error("Target not found")
        tuser = None
        guser = None
        for user in group.users:
            if(user.userId == current_user.id):
                guser = user
            if(user.userId == target.id):
                tuser = user
        beans = int(data.get('amount'))
        if(beans<=0):
            return bad_request_error("Invalid Amount")
        if(guser and tuser):
            if guser.beans>=beans:
                try:
                    Groups.objects(id=group.id, users__userId=current_user.id).update(dec__users__S__beans=beans)
                    Groups.objects(id=group.id, users__userId=target.id).update(inc__users__S__beans=beans)
                    
                    return success("Transfer Successful")
                except Exception as e:
                    return bad_request_error("Transfer failed")
            else:
                return bad_request_error("Insufficiant funds")
        else:
            return unauthorized_error("Users not in group")


