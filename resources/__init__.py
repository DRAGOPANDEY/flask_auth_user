# resources/__init__.py
from flask import Blueprint
from flask_restful import Api
from .user import UserProfileResource, UserProfileListResource, UserLoginResource, UserProfileDeleteResource, UserRegisterResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Define routes
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserProfileResource, '/users/<int:id>')
api.add_resource(UserProfileListResource, '/users')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserProfileDeleteResource, '/users/delete/<int:id>')
