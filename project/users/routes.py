from flask import Flask, request, jsonify
from .db import *

from project.users import users_blueprint

# app = Flask(__name__)
# # no need for CORS 

@users_blueprint.route('/users', methods=['GET'])
def getAllUsers():
    users = get_all_users()
    if users == None:
        return jsonify({}), 500
    return jsonify(users), 200


@users_blueprint.route("/user/<user_id>", methods=['GET'])
def getUser(user_id):
    user = get_user_by_id(user_id)
    if user == None:
        return jsonify({}), 500
    return jsonify(get_user_by_id(user_id)), 200


# used to modify and update an existing user record
@users_blueprint.route("/updateUser", methods=['POST'])
def postUser():
    # set data
    user = request.get_json()
    # we can maybe check the args later

    updated_user = update_user(user)
    if updated_user == None:
        return jsonify({}), 500

    return jsonify(updated_user), 200


# used to create a new user record, use /updateUser to overwrite
@users_blueprint.route("/insertUser", methods=['PUT'])
def putUser():
    user = request.get_json()
    inserted_user = insert_user(user)
    if inserted_user == None:
        return jsonify({}), 500

    return jsonify(inserted_user), 201


@users_blueprint.route("/deleteUser/<user_id>", methods=['DELETE'])
def deleteUser(user_id):
    res = delete_user(user_id)

    return jsonify(res), 200


@users_blueprint.route("/reset_table", methods=['DELETE'])
def resetTable():
    reset_table()

    return jsonify({}), 200
