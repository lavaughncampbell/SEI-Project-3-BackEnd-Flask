# this is like a user controller
# or auth controller

import models # get all the models. specifically user model

from flask import Blueprint, request # Blueprint is how we make our controllers

# make this a blueprint
users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
  return "user resource works"

# registration will be POST because were sending
# req.body there is going to be JSON
@users.route('/register', methods=['POST'])
def register():
  # this step is similar to making sure we can log
  # req.body in express.
  # note: we had to send JSON from postman(choose raw, select
  # JSON from the drop down menu, and type a perfect JSON object with
  # double qoutes around the keys
  print(request.get_json())
  return "check terminal"
