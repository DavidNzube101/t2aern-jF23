import ast
from flask import Flask, render_template, request, jsonify, Blueprint
import geocoder
from .database.db import dbORM
from .database.db import encrypt
from .utils import function_pool, id_generator
import json
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
    payload = function_pool.template_payload()
    
    with open("website/resources/available_subjects.json", "r") as f_:
        available_subjects = json.load(f_)
        
    payload['ASC'] = available_subjects
    payload['LengthFunc'] = len
    
    return render_template("index.html", **payload)


@routes.route('/s14xyu14xy14xyp14xye14xyr14xyu14xys14xye14xyr14xy14xy')
def returnsAdminDashBoard():
    
    return render_template("admin.html")