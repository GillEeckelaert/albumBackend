from flask import jsonify
from flask import current_app as app

@app.errorhandler(400)
def badRequest(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403