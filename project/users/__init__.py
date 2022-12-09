from flask import Blueprint

users_blueprint = Blueprint('users', __name__)

from project.users import routes

# app: project
# main: users