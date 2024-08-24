# resources/user.py

from flask_restful import Resource, reqparse
from flask import jsonify
from models import UserProfile, db
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app as app

class UserRegisterResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        parser.add_argument('address', type=str)
        parser.add_argument('phone_number', type=str)
        parser.add_argument('profile_picture', type=str)
        args = parser.parse_args()

        if UserProfile.query.filter_by(email=args['email']).first():
            return {'message': 'User already exists'}, 400

        user = UserProfile(
            username=args['username'],
            email=args['email'],
            password=args['password'],
            address=args.get('address'),
            phone_number=args.get('phone_number'),
            profile_picture=args.get('profile_picture')
        )
        db.session.add(user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

class UserProfileResource(Resource):
    @jwt_required()
    def get(self, id):
        user = UserProfile.query.get_or_404(id)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'address': user.address,
            'phone_number': user.phone_number,
            'profile_picture': user.profile_picture
        })

    @jwt_required()
    def put(self, id):
        user = UserProfile.query.get_or_404(id)
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('address', type=str)
        parser.add_argument('phone_number', type=str)
        parser.add_argument('profile_picture', type=str)
        args = parser.parse_args()

        if args['email']:
            user.email = args['email']
        if args['username']:
            user.username = args['username']
        if args['password']:
            user.password = args['password']
        if args['address']:
            user.address = args['address']
        if args['phone_number']:
            user.phone_number = args['phone_number']
        if args['profile_picture']:
            user.profile_picture = args['profile_picture']
        
        user.save()
        return jsonify({'message': 'User profile updated successfully.'})
    
    @jwt_required()
    def delete(self, id):
        user = UserProfile.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User profile deleted successfully.'})

class UserProfileListResource(Resource):
    @jwt_required()
    def get(self):
        users = UserProfile.query.all()
        return jsonify([{
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'address': user.address,
            'phone_number': user.phone_number,
            'profile_picture': user.profile_picture
        } for user in users])

class UserLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        user = UserProfile.query.filter_by(email=args['email']).first()
        print(user)
        print(check_password_hash(user.password, args['password']))
        if not user:
            return {'message': 'Invalid credentials: User not found'}, 401

        # Verify password
        if not user.password == args['password']:
            return {'message': 'Invalid credentials: Incorrect password'}, 401

        # Generate JWT token
        token = jwt.encode({
            'sub': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return {'token': token}, 200

class UserProfileDeleteResource(Resource):
    @jwt_required()
    def delete(self, id):
        user = UserProfile.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User profile deleted successfully.'})
