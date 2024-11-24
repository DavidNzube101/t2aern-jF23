import ast
from flask import Flask, redirect, render_template, request, jsonify, Blueprint, url_for
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
    
    try:
        client_ip = geocoder.ip('me').ip
    except:
        ip_address = request.remote_addr
        client_ip = ip_address
    
    with open("website/resources/available_subjects.json", "r") as f_:
        available_subjects = json.load(f_)
        
    available_upgrades = dbORM.get_all("AvailableUpgradesCRPS")
    
    user_history = function_pool.isFoundAll("HistoryCRPS", "crypsis_id", function_pool.checkLoginAndLogin(client_ip)['crypsis_id'])
        
    payload['AUP'] = available_upgrades
    # payload['ASC'] = available_subjects
    
    payload['LengthFunc'] = len
    payload['HISTORY_DATA'] = user_history
    payload['CRYPSIS_ID'] = function_pool.checkLoginAndLogin(client_ip)['crypsis_id']
    payload['SCHOOL_ID'] = function_pool.checkLoginAndLogin(client_ip)['school_id']
    payload['IP_ADDRESS'] = function_pool.checkLoginAndLogin(client_ip)['ip_address']
    payload['LOCATION'] = function_pool.checkLoginAndLogin(client_ip)['location']
    payload['LAT'] = function_pool.checkLoginAndLogin(client_ip)['latitude']
    payload['LNG'] = function_pool.checkLoginAndLogin(client_ip)['longitude']
    
    
    
    return render_template("index.html", **payload)


@routes.route("/update-school-id", methods=['POST'])
def updateSchoolID():
    crypsis_id = request.form['CRYPSIS_ID']
    school_id = request.form['school_id']
    
    dbORM.update_entry(
        "UserCRPS",
        f'{function_pool.isFound("UserCRPS", "crypsis_id", crypsis_id)}', 
        f'{encrypt.encrypter(str({"school_id": school_id}))}',
        dnd=False
    )
    
    return redirect(url_for('routes.returnLandingPage'))

@routes.route('/delete-history', methods=['POST'])
def deleteHistory():
    try:
        dbORM.delete_entry("HistoryCRPS", function_pool.isFound("HistoryCRPS", "history_id", request.form['history_id']))
        return jsonify({"message": "done"})
    
    except Exception as e:
        return jsonify({"message": ["error", e]})
    
    
@routes.route("/add-upgrade-request", methods=['POST'])
def addUpgrade():
    try:
        amount = request.form['amount']
        upgrade_ids = ast.literal_eval(request.form['upgrade_ids'])
        print("westwern", upgrade_ids, request.form['upgrade_ids'])
        crypsis_id = request.form['crypsis_id']
        paidUpgradesDescription = []
        
        for upgrade_id in upgrade_ids:
            theUpgrade = dbORM.get_all("AvailableUpgradesCRPS")[f'{function_pool.isFound("AvailableUpgradesCRPS", "upgrade_id", upgrade_id)}']
            paidUpgradesDescription.append(theUpgrade['theupgrade'])
            
            new_upgrade = {
                "name": theUpgrade['name'],
                "theupgrade": theUpgrade['theupgrade'],
                "school_id": dbORM.get_all("UserCRPS")[f'{function_pool.isFound("UserCRPS", "crypsis_id", crypsis_id)}']['school_id'],
                "status": "new",
                "datestamp": function_pool.getDateTime()[0],
                "timestamp": function_pool.getDateTime()[1],
                "upgrade_id": theUpgrade['upgrade_id'],
                "crypsis_id": crypsis_id
            }
            dbORM.add_entry("UpgradeCRPS", encrypt.encrypter(str(new_upgrade)))
            
            
        upgrades_string = ", ".join(paidUpgradesDescription)
        new_history = {
            "narration": f"Paid for {upgrades_string}",
            "amount": amount,
            "crypsis_id": crypsis_id,
            "datestamp": function_pool.getDateTime()[0],
            "timestamp": function_pool.getDateTime()[1],
            "history_id": id_generator.generate_id(16)
        }
        dbORM.add_entry("HistoryCRPS", encrypt.encrypter(str(new_history)))
        
        
        
        return jsonify({"message": "done"})
    
    except Exception as e:
        return jsonify({"message": ["error", e]})