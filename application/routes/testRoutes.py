# app.py
from flask import request, jsonify, Blueprint


testRoutesBlueprint = Blueprint('testRoutes', __name__)

@testRoutesBlueprint.route('/')
def index():
    return "<h1>Album Python Backend</h1>"

@testRoutesBlueprint.route('/test/', methods=['GET'])
def test():
    # Retrieve the name from url parameter
    arg = request.args.get("arg", None)

    # For debugging
    print("Hello World")

    response = {}

    # Check if user sent a name at all
    if not arg:
        response["ERROR"] = "No argument given."
    # Check if the user entered a number not a name
    elif str(arg).isdigit():
        response["ERROR"] = "Argument must be string."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Test using {arg} was succesful."

    # Return the response in json format
    return jsonify(response)
