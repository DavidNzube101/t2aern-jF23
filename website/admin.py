import ast
from flask import Flask, render_template, request, jsonify, Blueprint
import geocoder
from .database.db import dbORM
from .database.db import encrypt
from .utils import function_pool, id_generator
from werkzeug.security import generate_password_hash, check_password_hash


admin = Blueprint('admin', __name__)

@admin.route('/s14xyu14xy14xyp14xye14xyr14xyu14xys14xye14xyr14xy14xy')
def returnsAdminDashBoard():
    payload = function_pool.template_payload()
    
    payload['UPGRADES'] = dbORM.get_all("UpgradeCRPS")
    
    return render_template("admin.html", **payload)


@admin.route("/mark-upgrade-as-done", methods=['POST'])
def markUpgradeAsDone():
    status = request.form['status']
    upgrade_id = request.form['upgrade_id']
    
    dbORM.update_entry(
        "UpgradeCRPS",
        f'{function_pool.isFound("UpgradeCRPS", "upgrade_id", upgrade_id)}', 
        f'{encrypt.encrypter(str({"status": status}))}',
        dnd=False
    )
    
    return jsonify({"message": "done"})