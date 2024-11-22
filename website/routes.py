import ast
from flask import Flask, render_template, request, jsonify, Blueprint
import geocoder
from .database.db import dbORM
from .database.db import encrypt
from .utils import function_pool, id_generator
from werkzeug.security import generate_password_hash, check_password_hash


routes = Blueprint('routes', __name__)

@routes.route('/')
def returnLandingPage():
    payload = function_pool.template_payload()
    
    session_id = id_generator.generate_id(256)
    
    payload['SESSION_ID'] = session_id
    
    return render_template("landing.html", **payload)

@routes.route('/≏⁕/<string:session_id>/¬⁎⁌⁍;')
def returnDashBoard(session_id):
    
    return render_template("index.html")