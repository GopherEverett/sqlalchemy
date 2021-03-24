from flask import Flask
from flask_restful import Api
from resources.user import Users, SingleUser

app = Flask(__name__)

api = Api(app)

# Init db and migrate here

# Init db and migrate here

# Leave resources
api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
