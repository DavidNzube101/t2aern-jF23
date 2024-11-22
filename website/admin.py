import ast
from flask import Flask, request, jsonify, Blueprint
import geocoder
from .database.db import dbORM
from .database.db import encrypt
from .utils import function_pool, id_generator
from werkzeug.security import generate_password_hash, check_password_hash


admin = Blueprint('admin', __name__)