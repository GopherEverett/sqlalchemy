from flask_restful import Resource
from flask import request
from models.user import User
from models.db import db
# Import user and db here


class Users(Resource):
    def get(self):
        data = User.find_all()
        results = [u.json() for u in data]
        return results

    def post(self):
        data = request.get_json()
        user = User(**data)
        user.create()
        return user.json(), 201


class SingleUser(Resource):
    def get(self, id):
        data = User.find_by_id(id)
        return data.json()

    def delete(self, id):
        data = User.delete_user(id)
        return data

    def put(self, id):
        data = User.update_user(id)
        return data
