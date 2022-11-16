# Flask SQLAlchemy

![](https://i.ytimg.com/vi/_ts6qss1hVw/maxresdefault.jpg)

## Overview

In this lesson, we'll learn how to interact with a postgres database using `SQLAlchemy` and `Flask`. `SQLAlchemy` is an ORM similar to `Sequelize`. It allows us to model our data and interact with it in a simple way. We'll also learn how to utilize migrations to track changes to our database using `Flask Migrate`.

## Getting Started

- Fork and Clone
- `virtualenv venv`
- `source venv/bin/activate`
- `pip3 install -r requirements.txt`

## Adding SQLAlchemy To The Mix

In order to use `SQLAlchemy` we'll need to install it along with the correct database driver.

Let's install the necessary packages:

```sh
pip3 install flask-sqlalchemy psycopg2-binary flask-migrate
```

Now that we've installed the necessary packages, let's save them to our `requirements.txt`:

```sh
pip3 freeze > requirements.txt
```

### Setting Up The SQLAlchemy Instance

In `models/db.py` let's import `SQLAlchemy` and create a new instance of it:

```py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

By creating a new instance of `SQLAlchemy`, we'll be able to use it anywhere in our flask app. The `db` variable contains all of the methods and attributes we'll need in order to link our app and provide our models with the necessary information.

### Linking Our Flask App

Open `app.py`. We'll need to link `SQLAlchemy` to our flask app in order to interact with our database.

Let's start by importing a few things in `app.py`:

```py
from flask_migrate import Migrate
from models.db import db
```

Next we need to set up some configuration for our app:

```py
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_db"
app.config['SQLALCHEMY_ECHO'] = True
```

The first line stops our database from tracking modifications of objects. Why is this important? Every time we make a change to our models, `SQLAlchemy` caches those changes which can lead to high memory usage by our application. By default it's set to `None` which will emit a warning.

The second line tells `SQLAlchemy` what database to use.

And finally the last line turns on `SQL` statement logging for debugging.

**`Note: This should be turned off in a production environment`**.

Next we'll link our `Flask` app to our ORM and link both the `app` and `db` to the migration library:

**A comment block has been provided for you. Put the next snippet within those comments.**

```py
db.init_app(app)
migrate = Migrate(app, db)
```

## Creating Models

We'll now set up our first model. Let's start with a simple one `User`. Open the `models/user.py` file.

You should have the following class:

```py
class User:
    pass
```

Let's start by importing a couple of things:

```py
from datetime import datetime
from models.db import db
```

We're using the `datetime` module to generate some timestamps for us and importing our `db` instance in order for our model to inherit some functionality.

First we need to have our `User` class inherit from our `db` instance. We'll inherit the `Model` attribute from our instance:

```py
class User(db.Model):
    pass
```

Next we need to declare the `tablename` for our model:

```py
class User(db.Model):
    # defines table name
    __tablename__ = 'users'
```

`__tablename__` is a special variable from `SQLAlchemy` that allows us to define a table name.

### Defining Columns

Now we'll define the columns for our user. It should have the following:

- `id`
- `name`
- `email`
- `password`
- `created_at`
- `updated_at`

Add the following below the `__tablename__` variable:

```py
id = db.Column(db.Integer, primary_key=True)
name = db.Column(db.String(80))
email = db.Column(db.String(255))
password = db.Column(db.String(255))
created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.now())
```

Finally we'll set up a contructor for our `User` model:

```py
def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password
```

Notice how we do not pass the `created_at` and `updated_at` fields into the contructor, those fields are set to default. The ORM will handle inputting those values for us.

### Executing Migrations

Now that our `Model` is set up, we can create our database and migrate these changes.

**NOTE: This step is important, if this is forgotten, the migrations will not work.**

First we need to import our model into `app.py`:

```py
from models.user import User
```

Without importing our models, the migration script won't be able to keep track of what it looks like and what changes we've made over time.

Run the following in your terminal:

```sh
createdb flask_db
```

```sh
flask db init
```

```sh
flask db migrate -m "<some message>"
```

```sh
flask db upgrade
```

Let's confirm that our table was created correctly:

```sh
psql flask_db
```

```SQL
SELECT * FROM users;
```

Your table should resemble the following:

```
+------+--------+---------+------------+--------------+--------------+
| id   | name   | email   | password   | created_at   | updated_at   |
|------+--------+---------+------------+--------------+--------------|
+------+--------+---------+------------+--------------+--------------+
```

### Querying

Now that our table is created, we're ready to start building some queries!

Let's create a couple of methods for our model. We'll start with building in the ability to view our data in a `JSON` serializable format. Add the following to your `User` model.

```py
def json(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "created_at": str(self.created_at),
                "updated_at": str(self.updated_at)}
```

#### **Create**

Next let's add the ability to create a user:

```py
def create(self):
        db.session.add(self)
        db.session.commit()
        return self
```

Let's break this down:

- We provide `self` as an argument which will give us the attributes for the user instance.
- The `db.session.add` method provides the necessary data to `SQLAlchemy` in order to perform an `insert`, `SQLAlchemy` handles putting the fields in the proper order.
- `db.session.commit` saves the record. The `commit` method is standard across databases.

#### **Get**

Now we'll build in the functionality to get multiple records. Add the following to your `User` model:

```py
@classmethod
def find_all(cls):
    return User.query.all()
```

Notice a few things here:

- The `@classmethod` decorator binds a function to the class rather than an instance itself. This allows us to use it without have to create a new instance of the `User`.
- The `cls` argument is short for `class`. It provides us with information if required about our `class`. It is also a required argument when declaring a `classmethod`.
- The `query` object is built into `User` because we are inheriting from `db.Model`.

#### **Get By Id**

Finally let's build in the functionality to find a user by id:

```py
@classmethod
def find_by_id(cls, id):
    return User.query.filter_by(id=id).first()
```

## Integrating The Model Into Our Api

Now that we've set up our model, we're ready to integrate it into our Api.

Let's start by finding `resources/user.py`

You'll notice there are two resources, a `Users` resource and `SingleUser`. The `Users` resource will handle requests for `/users` and `SingleUser` will handle the requests for `/users/<int:id>`.

Let's first import our `User` model and our `db` instance:

```py
from models.user import User
from models.db import db
```

### Getting All Users

We'll start with getting multiple users. In the `Users` resources `get` method, we'll start by querying for all users:

```py
def get(self):
    data = User.find_all()
    results = [u.json() for u in data]
    return results
```

The `find_all` method returns a list with instances of each user. We loop through all of the users found using `list comprehension` and parse them all using the `json` method we created earlier.

We then return the list of users.

### Creating a User

Let's now create a user. In the `Users` `post` method, add the following:

```py
def post(self):
    data = request.get_json()
    user = User(**data)
    user.create()
    return user.json(), 201
```

Notice the `**` operator, that is the `python` version of the `object spread` operator.

### Testing

Now that we have functionality to `GET` and `CREATE` users, let's test these endpoints in `Insomnia`.

Start your flask app with `python3 app.py`.

- [POST] `http://localhost:5000/users`
- [GET] `http://localhost:5000/users`

## You Do

Utilizing the [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/) docs, build the functionality for the `SingleUser` resource.

Test your endpoints using insomnia each step of the way.

## Recap

In this lesson, we learned how to define models using `Flask SQLAlchemy` and how to perform `CRUD` operations on our model with `Flask Restful`. In the coming lessons, we'll learn how to set up associations and joins with `SQLAlchemy`.

## Resources

- [Python Class Methods](https://www.programiz.com/python-programming/methods/built-in/classmethod)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

## Location

```geojson
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [
                            33.730565,
                            -84.38078
                ]
            }
        }
    ]
}