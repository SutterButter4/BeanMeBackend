# flask packages
from flask_restful import Api

from api.api import root, getUser, notifications, notifications
# project resources
from api.auth import SignUpApi, LoginApi
from api.group import getGroupTasks, getGroup, groupInvite, acceptInvite, makeGroup, transfer
from api.task import schedule_task, makeTask, taskId, taskCommit


def create_routes(api: Api):
    api.add_resource(root, '/')

    #User
    api.add_resource(SignUpApi, '/auth/signup')
    api.add_resource(LoginApi, '/auth/login')

    api.add_resource(getUser, '/user')
    api.add_resource(notifications, '/notifications')


    #Groups
    api.add_resource(getGroup, '/groups')
    api.add_resource(makeGroup, '/groups/create')
    api.add_resource(getGroupTasks, '/groups/tasks')
    api.add_resource(groupInvite, '/groups/invite') #invite notif DONE
    api.add_resource(acceptInvite, '/groups/accept-invite') #user joined notif DONE
    api.add_resource(schedule_task, '/groups/schedule-task')
    api.add_resource(transfer, '/groups/transfer') #transfer notif


    #Tasks
    api.add_resource(taskId, '/tasks')
    api.add_resource(taskCommit, '/tasks/commit') #if task fullfilled, notif
    api.add_resource(makeTask, '/tasks/make') #task created notif
    # api.add_resource(makeComplete, '/tasks/complete')