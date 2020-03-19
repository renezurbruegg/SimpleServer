# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point for the server application."""
import json
import logging
import os
import traceback
from datetime import date
from datetime import timedelta, datetime
from functools import update_wrapper

from bson.objectid import ObjectId
from flask import make_response
from flask import request, current_app, Flask
from flask_cors import CORS
from flask_jwt_simple import (
    JWTManager
)
import collections
from pylogging import HandlerType, setup_logger
from pymongo import MongoClient

from .config import CONFIG
from .http_codes import Status

# Configure log files
logger = logging.getLogger(__name__)
setup_logger(log_directory='./logs', file_handler_type=HandlerType.ROTATING_FILE_HANDLER, allow_console_logging = True, console_log_level  = logging.DEBUG, max_file_size_bytes = 1000000)
app = Flask(__name__)

# Load Configuration for app. Secret key etc.
config_name = os.getenv('FLASK_CONFIGURATION', 'default')
app.config.from_object(CONFIG[config_name])

# Set Cors header. Used to accept connections from browser using XHTTP requests.
CORS(app, headers=['Content-Type'])
jwt = JWTManager(app)

# Database name
app_name = "test_app"
# Collections name
userCollection = "users"

# Open up database
database = MongoClient("localhost", 27017)[app_name]


def main():
    """Main entry point of the app. """

    logger.info("starting server")
    try:
        app.run(debug = True, host = app.config["IP"], port = app.config["PORT"])
        logger.info("Server started. IP: " + str(app.config["IP"]) + " Port: " + str(app.config["PORT"]))
    except Exception as exc:
        logger.error(exc)
        logger.exception(traceback.format_exc())
    finally:
        pass

# This makes sure that only trusted user (after having signed in) can access the server
# Not used right now
@jwt.jwt_data_loader
def add_claims_to_access_token(identity):
    now = datetime.utcnow()
    return {
        'exp': now + current_app.config['JWT_EXPIRES'],
        'iat': now,
        'nbf': now,
        'sub': identity,
        'roles': 'Admin'
    }



# This is here so browser do not complain about CORS header.
# It makes sure that website that are not hosted on this server, can access the api.
def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Content-type'] = "application/json"
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator




#-------------------------------------------------------------------------------
#                       BEGIN API Functions
#-------------------------------------------------------------------------------
# @jwt_required # Make sure only user that logged in can use this route
@app.route('/api/listUser', methods=['GET', 'OPTIONS']) # This is a GET request (can be viewed in browser)
@crossdomain(origin = '*') # make sure other website can access this link too
def listUsers():
    users = []
    collection = database[userCollection] # open user collection

    for entry in collection.find():
        users.append(entry['name']) # add each name of an entry of the user collection to the users list

    users_as_json = json.dumps(users, indent=2, sort_keys=False) # convert list object to JSON format

    return users_as_json, Status.HTTP_OK_ACCEPTED

@app.route('/api/addUser', methods=['POST', 'OPTIONS']) # This is a post request. Need postman for this
@crossdomain(origin = '*')
def addUser():
    # get params from post request
    params = request.get_json()
    name = params['name']

    userObj = {'name': name} # creates a python dictionery object to insert into the user database

    collection = database[userCollection] # open user collection
    collection.insert(userObj)

    return "Added User", Status.HTTP_OK_BASIC








