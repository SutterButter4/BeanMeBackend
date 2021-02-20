from flask import Flask
from flask import jsonify

# from flask_login import LoginManager
# import pymongo

app = Flask(__name__)
# login_manager = LoginManager()
# login_manager.init_app(app)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)
#
#         flask.flash('Logged in successfully.')
#
#         next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         if not is_safe_url(next):
#             return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)

@app.route('/')
def root():
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")

@app.route('/users')
def user():
    return 'users'

@app.route('/users/sigin')
def signin():
    return 'users/signin'

#
# #accessing stuff from mongodb
# DATABASE_NAME = ""
# COLLECTION_NAME = ""
# client = pymongo.MongoClient("mongodb+srv://admin:TvUPRBOAGTn6lBBL@cluster0.fv5vo.mongodb.net/beanme?retryWrites=true&w=majority")
# #database name
# db = client[DATABASE_NAME]
#
# #collection name
# coll = db[COLLECTION_NAME]
#


