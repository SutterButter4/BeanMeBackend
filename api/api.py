# flask packages
import jwt
from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

# project resources
from models.user import Users
from models.group import Groups,GroupUser
from models.task import Tasks


from api.error import unauthorized




#return the single user that called this method from the front end
class getUser(Resource):
    @jwt_required
    def post(self):
        return current_user



class groupsName(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        result = Groups.objects.get(name=data.name)
        if not result:
            return "BAD REQUEST", 400
        else:
            return result, "OK", 201

class groupsID(Resource):
    @jwt_required
    def get(self, id):
        result = Groups.objects.get(id=id)
        if not result:
            return "BAD REQUEST", 400
        else:
            return result, "OK", 201

    def delete(self,id):
        result = Groups.objects.get(id=id)

# a user inviting another user to a certain group
class getGroupTasks(Resource):
    @jwt_required
    def post(self, id):
        result = Groups.objects.get(id=id).tasks
        if not result:
            return "BAD REQUEST", 400
        else:
            return result, "OK", 201


#a user inviting another to a group
class groupInvite(Resource):
    @jwt_required
    def post(self):

        data = request.json()
        userID = data.userID
        groupID = data.groupID

        try:
            user = Users.objects.get(id=userID)
        except:
            return "USER NOT FOUND", 404,

        try:
            group = Groups.objects.get(id=groupID)
        except:
            return "UNAUTHORIZED", 401

        try:
            group.invitedUsers.objects.get(id=current_user.id)
        except:
            return "UNAUTHORIZED", 401

        group.update(
            add_to_set__invitedUsers=user.id
        )

        return groupID


class acceptInvite(Resource):
    @jwt_required
    def post(self):
        #if user is in list of invites, add to group and remove from invites
        data = request.get_json()
        try:
            group = Groups.objects.get(id=data.GroupId)
        except:
            return "NO GROUP FOUND", 404
        else:
            if current_user.id in group.invitedUsers:

                # remove user from this group's invites
                group.update(unset__invitedUsers=current_user.id)
                # add user to the group
                newUser = GroupUser(userId=current_user.id,beans=0)
                group.update(add_to_set__users=newUser)

            else:
                return "NO INVITE FOUND", 404





#add task to group
#TaskId, Interval(ms) --> group
class schedule_task(Resource):
    @jwt_required
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

        Groups.objects

        group.update




class transfer(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            group = Groups.objects.get(id=data.get('group_id'))
        except:
            return "GROUP NOT FOUND", 404

        if current_user.id in group.users and data.get('TargetUser') in group.users:
            amount = data.get('Amount')
            group.update()
        pass


class taskName(Resource):
    @jwt_required
    def post(self):
        pass


class taskID(Resource):
    @jwt_required
    def post(self):
        pass


class taskCommit(Resource):
    @jwt_required
    def post(self):
        pass
