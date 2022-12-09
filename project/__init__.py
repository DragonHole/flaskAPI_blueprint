from flask import Flask
#from project.users.db import * # this excludes the module private methods
 
def create_app():
    app = Flask(__name__)

    # register_blueprints(app)
    # potentially add more preparations here
    from project.users import users_blueprint
    app.register_blueprint(users_blueprint)

    return app


# def register_blueprints(app):
#     # Since the application instance is now created, register each Blueprint
#     # with the Flask application instance (app)
#     from project.users import users_blueprint

#     app.register_blueprint(users_blueprint)
