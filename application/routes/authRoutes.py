from flask import request, jsonify, Blueprint


authRoutesBlueprint = Blueprint('authRoutes', __name__)

@authRoutesBlueprint.route('/login', methods=['GET', 'POST'])
def login():
    return "<h1>Album Python Backend</h1>"

