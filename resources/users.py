# this is like a user controller
# or auth controller

import models # get all the models. specifically user model

from flask import Blueprint, request, jsonify # Blueprint is how we make our controllers

from flask_bcrypt import generate_password_hash # to generate password hash
                        # this is a function that returns a scrambled pw

from playhouse.shortcuts import model_to_dict
# we can jsonify our models with this import

# make this a blueprint
users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
  return "user resource works"


# REGISTRATION PROCESS //


# registration will be POST because were sending
# req.body there is going to be JSON
@users.route('/register', methods=['POST'])
def register():
  # this step is similar to making sure we can log
  # req.body in express.
  # note: we had to send JSON from postman(choose raw, select
  # JSON from the drop down menu, and type a perfect JSON object with
  # double qoutes around the keys
  payload = request.get_json()
  print(payload)

  # since emails are case insensitive in the world
  # this makes the email lowercase
  payload['email'] = payload['email'].lower()
  # might as well do the same with username
  payload['username'] = payload['username'].lower()
  print(payload) # that's better

# see if the user exists
  try:

    models.User.get(models.User.email == payload['email'])
  # this will throw an eror ()
  # shortcut method for select().where().execute_query is .get()
# if so -- we don't want to create the user
  # response: "user with that email already exist"
    return jsonify(
      data={},
      message="A user with that email already exists",
      status=401
    ), 401

# if the user does not exist
  except models.DoesNotExist: # except is like catch in JS
  # create them!

    pw_hash = generate_password_hash(payload['password'])

    created_user = models.User.create(
      username=payload['username'],
      email=payload['email'],
      password=pw_hash,
      name=payload['name'],
      bootcamp=payload['bootcamp'],
      position=payload['position']
    )

    print(created_user)

    # respond with new object and success message

    # jsonify our models
    created_user_dict = model_to_dict(created_user)
    # we can't jsonify the password (generate_password_has gives us
    print(type(created_user_dict['password']))
    # this will get rid of the error
    created_user_dict.pop('password')

    return jsonify(
      data=created_user_dict,
      message="Successfully registered user",
      status=201
    ), 201
