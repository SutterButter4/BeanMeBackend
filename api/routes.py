# flask packages
from flask_restful import Api

# project resources
from api.auth import SignUpApi, LoginApi
from api.api import getUser, getGroupTasks, groupsName, groupsID, groupInvite, acceptInvite, schedule_task, transfer, \
    taskName, taskID, taskCommit, hello


def create_routes(api: Api):
    api.add_resource(hello, '/hello')


    #Auth
    api.add_resource(SignUpApi, '/auth/signup/')
    api.add_resource(LoginApi, '/auth/login/')

    api.add_resource(getUser, '/getUser')
    #Groups

    api.add_resource(groupsName, '/groups')
    api.add_resource(groupsID, '/groups/<int:id>')
    api.add_resource(getGroupTasks, '/groups/<int:id>/tasks')
    api.add_resource(groupInvite, '/groups/invite')
    api.add_resource(acceptInvite, '/groups/accept-invite')
    api.add_resource(schedule_task, '/groups/schedule-task')
    api.add_resource(transfer, '/groups/transfer')


    #Tasks
    api.add_resource(taskName, '/tasks')
    api.add_resource(taskID, '/tasks/<int:id>')
    api.add_resource(taskCommit, '/tasks/commit')