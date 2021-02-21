# flask packages

import json
import sys

from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from api.response import bad_request_error, not_found_error, unauthorized_error, success
from models.group import Groups, GroupUser
# project resources
from models.notifications import Notifications
from models.user import Users
from models.task import Tasks

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
        #try:
        group.save()

        #except:
            #return bad_request_error("Could not save group")
        try:
            Users.objects(id=current_user.id).update_one(push__groups=group.id)
            return success(group.to_json())
        except Exception as e:
            group.delete()
            return bad_request_error(str(e))

#get all tasks in a group
class getGroupTasks(Resource):
    @jwt_required()
    def post(self):
        id = request.json.get('groupId')
        try:
            group = Groups.objects.get(id=id)
        except Exception as e:
            return not_found_error("Group not found")

        if group.id not in current_user.groups:
            return unauthorized_error("User not in group")

        result = Tasks.objects(groupId=group.id)

        return success(result.to_json())

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

        if group.id in list(user.invites):
            return bad_request_error("user already invited to group")

        if group.id in list(user.groups):
            return bad_request_error("user already in group")
        try:
            user.update(add_to_set__invites=group.id)
        except Exception as e:
            return bad_request_error("Could not invite user")

        #create notification:
        notif = Notifications(type="INVITE", userOwnerId=user.id, groupId=group.id)
        notif.save()
        user.update(add_to_set__notificationIds=notif.id)

        return success()


class acceptInvite(Resource):
    @jwt_required()
    def post(self):
        #get group
        try:
            group = Groups.objects.get(id=request.json.get('groupId'))
        except:
            return not_found_error("Group not found")

        if not (group.id in current_user.invites):
            return not_found_error("No invite to this group")

        # remove invite from user profile
        current_user.update(pull__invites=group.id)
        current_user.update(push__groups=group.id)

        # add user to the group
        newUser = GroupUser(userId=current_user.id,beans=10)
        group.update(add_to_set__users=newUser)

        #notify all group members except one added
        users_in_group = []

        for user in group.users:
            try:
                users_in_group.append(Users.objects.get(id=user.userId))
            except:
                pass

        notifs = []
        for user in users_in_group:
            notifs.append(Notifications(type="USER_JOINED", userOwnerId=user.id, groupId=group.id, userTopicId=current_user.id))

        for notif in notifs:
            notif.save()
            Users.objects.get(id=notif.userOwnerId).update(push__notificationIds=notif.id)

        return success(group.to_json())

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
            if user.userId == current_user.id:
                guser = user
            if user.userId == target.id:
                tuser = user
        beans = int(data.get('amount'))
        if beans<=0:
            return bad_request_error("Invalid Amount")
        if guser and tuser:
            if guser.beans>=beans:
                try:
                    Groups.objects(id=group.id, users__userId=current_user.id).update(dec__users__S__beans=beans)
                    Groups.objects(id=group.id, users__userId=target.id).update(inc__users__S__beans=beans)

                except Exception as e:
                    return bad_request_error("Transfer failed")
                # create notification:
                try:
                    notif = Notifications(type="INCOMING_TRANSFER", userTopicId=current_user.id, groupId=group.id, beanCount=beans)
                    notif.save()
                    target.update(push__notificationIds=notif.id)
                except:
                    bad_request_error("Failed to make notification")

                if guser.beans == 0:
                    try:
                        # notify all group members except one added
                        users_in_group = list(Users.objects(id=[user.userId for user in group.users]))
                        notifs = [Notifications(type="OUT_OF_BEANS", userOwnerId=user.id, userTopicId=current_user.id,groupId=group.userId) for user
                                  in users_in_group]
                        for notif in notifs:
                            notif.save()
                            Users.objects.get(id=notif.userOwnerId).update(push__notificationIds=notif.id)

                    except:
                        bad_request_error("Failed to make notification")

                return success()
            else:
                return bad_request_error("insufficient funds")
        else:
            return unauthorized_error("Users not in group")


