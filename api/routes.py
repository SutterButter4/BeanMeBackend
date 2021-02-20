# flask packages
from flask_restful import Api

# project resources
from api.auth import SignUpApi, LoginApi
from api.api import root, getUser
from api.group import getGroupTasks, getGroup, groupInvite, acceptInvite, makeGroup
from api.task import schedule_task, transfer, \
    makeTask, taskID, taskCommit

def create_routes(api: Api):
    api.add_resource(root, '/')

    #Auth
    api.add_resource(SignUpApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')

    api.add_resource(getUser, '/getUser')

    #Groups
    api.add_resource(getGroup, '/groups')
    api.add_resource(makeGroup, '/groups/create')
    api.add_resource(getGroupTasks, '/groups/<int:id>/tasks')
    api.add_resource(groupInvite, '/groups/invite')
    api.add_resource(acceptInvite, '/groups/accept-invite')
    api.add_resource(schedule_task, '/groups/schedule-task')
    api.add_resource(transfer, '/groups/transfer')


    #Tasks
    api.add_resource(taskID, '/tasks    ')
    api.add_resource(taskCommit, '/tasks/commit')
    api.add_resource(makeTask, '/tasks/make')