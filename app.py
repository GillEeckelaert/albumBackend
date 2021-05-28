# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/test/', methods=['GET'])
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

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)