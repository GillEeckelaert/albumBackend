# app.py
from flask import request, abort, Blueprint, make_response, jsonify
from datetime import datetime as dt
from flask import current_app as app
from ..models.models import db, User
from ..controllers import user_controller

userRoutesBlueprint = Blueprint('userRoutes', __name__)

@userRoutesBlueprint.route('/adduser/', methods=['GET'])
async def addUser():
    username = request.args.get('user')
    email = request.args.get('email')

    if username and email:
        userExists = await user_controller.checkExistingUser(username, email)
        if userExists:
            abort(403, description="User already exists.")

        new_user = User(
            username=username,
            email=email,
            created=dt.now(),
            admin=False
        )
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
    else:
        abort(400, description="Not all parameters that are obligated were given.")
    return make_response(f"{new_user} successfully created!")

@userRoutesBlueprint.route('/users/', methods=['GET'])
async def getAllUsers():
    users = User.query.all()
    print(users)
    return make_response(f"Returned all users")