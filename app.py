from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.user import Users, SingleUser
from flask_migrate import Migrate
from models.db import db
from models.user import User

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_db"
app.config['SQLALCHEMY_ECHO'] = True
# Init db and migrate here
db.init_app(app)
migrate = Migrate(app, db)
# Init db and migrate here

# Leave resources
api.add_resource(Users, '/users')
api.add_resource(SingleUser, '/users/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
