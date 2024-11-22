from ..database.db import dbORM
import base64
import imghdr
from flask import jsonify
import datetime as dt
import json
from datetime import datetime, timedelta, date
import random
from flask_login import login_required, current_user
from typing import TypedDict, Dict, List, Optional
from . import DateToolKit as dtk
import math as Math
from . import id_generator
import ast
from ..database import encrypt


def template_payload()-> dict:
    return {}

def calcTimeDifference(dpt, ct):
	return [int(x) for x in ("[" + str(datetime.strptime(dpt, "%H:%M") - datetime.strptime(ct, "%H:%M:%S")).replace(":", ", ").replace("-1 day, ", "") + "]").strip("[]").split(", ")]

def isFound(model, column, value):
	if dbORM.find_one(model, column, value)['status'][0] == "not found":
		result = None
	else:
		# print(isFound(model, column, value))
		result = dbORM.find_one(model, column, value)['status'][1]

	# print(">>>>>>><><><><><>>>>>>>>>>>>> ", result, " ", isFound(model, column, value))
	return result

def returnJSONData(title, content):
	return jsonify({
		"message": {title: content}
	})
 
def getDepartmentFaculty(department):
    return department

def isFoundAll(model, column, value):
	if dbORM.find_all(model, column, value)['status'][0] == "not found":
		result = []
	else:
		# print(isFound(model, column, value))
		result = dbORM.find_all(model, column, value)['status'][1]

	# print(">>>>>>><><><><><>>>>>>>>>>>>> ", result, " ", isFound(model, column, value))
	return result



def extract_birth_dates(_data):
    print(_data)
    data_list = eval(str(_data))
    data = data_list[0]
    print(type((data)), data)
    
    birth_dates = []
    
    for cv in range(len(_data)): # column, value
        date_str = data['date_of_birth']
        if date_str and date_str != "NULL":
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                birth_dates.append({
				'user_id': data['id'],
				'month': date_obj.strftime('%B'),  # Full month name
				'year': date_obj.year
				})
            except ValueError:
                continue
    
    return birth_dates

def get_user_birth_date(data, user_id):
    """
    Get birth month and year for a single user by their ID.
    
    Parameters:
    data (dict): The complete user data dictionary
    user_id (str): The ID of the user to look up
    
    Returns:
    dict: Dictionary containing month and year, or None if not found/invalid
    """
    # Convert user_id to string if it isn't already
    user_id = str(user_id)
    
    # Check if user exists
    if user_id not in data:
        return {
            "error": f"User with id `{user_id}` not found",
            "success": False
        }
    
    # Get user data
    user = data[user_id]
    date_str = user.get('date_of_birth')
    
    # Check if date exists and is valid
    if not date_str or date_str == "NULL":
        return {
            "error": "No birth date available for this user",
            "success": False
        }
    
    try:
        # Parse the date string
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        return {
            "success": True,
            "data": {
                "month": date_obj.strftime('%B'),  # Full month name
                "year": date_obj.year,
                "user_name": f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or "No name provided"
            }
        }
    except ValueError:
        return {
            "error": "Invalid date format",
            "success": False
        }

def loopAppendAndReverse(a, b):
	try:
		for k, v in a.items():
			b.append(v)
		return b[::-1]
	except Exception as e:
		return f"Error occured\nError: {e}"

def toJoin(i, j):
	return f"{i}{j}"

def thousandify(amount):
	amount = "{:,}".format(float(amount))
	return f"{amount}"

def is_test():
	return "True"

def floatToInt(n):
	return f"{Math.ceil(float(n))}"

def StandardCurrency():
	return "NGN"

def returnJSONData(title, content):
	return jsonify({
		"message": {title: content}
	})

from typing import Dict, List, TypedDict, Any
from datetime import datetime, timedelta



class UserData(TypedDict):
    email: str
    reg_number: str
    first_name: str
    last_name: str
    profile_image: Optional[str]  # Made this optional if it's not always present
    bio: Optional[str]
    following: Optional[str]  # Double-check if this is a string, it might be a list
    followers: Optional[str]  # Same as above
    date_joined: str
    date_of_birth: Optional[str]
    department: Optional[str]
    username: str
    password: str
    interests: Optional[str]
    id: str
    user_unique_id: str

def get_recent_users(users_data: Dict[str, UserData], days: int = 5) -> List[UserData]:
    """
    Filter users who joined within the specified number of days.
    
    Args:
        users_data (Dict[str, UserData]): Dictionary of user data
        days (int): Number of days to look back (default: 5)
    
    Returns:
        List[UserData]: List of users who joined within the specified period
    """
    # Get current date
    current_date = datetime.now()
    
    # Calculate the cutoff date
    cutoff_date = current_date - timedelta(days=days)
    
    # Filter recent users
    recent_users = []
    
    for user_id, user_data in users_data.items():
        try:
            # Convert date_joined string to datetime object
            join_date = datetime.strptime(user_data['date_joined'], '%Y-%m-%d')
        except ValueError:
            continue  # Skip users with invalid date_joined format
        
        # Check if user joined after cutoff date
        if join_date >= cutoff_date:
            recent_users.append(user_data)
    
    # Sort by date_joined (most recent first), convert to datetime in the sort key
    recent_users.sort(key=lambda x: datetime.strptime(x['date_joined'], '%Y-%m-%d'), reverse=True)
    
    return recent_users

# # Example usage:
# def print_recent_users(users_data: Dict[str, Any]) -> None:
#     """
#     Print information about recently joined users.
    
#     Args:
#         users_data (Dict[str, Any]): Dictionary of user data
#     """
#     recent_users = get_recent_users(users_data)
    
#     print(f"Users who joined in the last 5 days ({len(recent_users)} users):")
#     print("-" * 50)
    
#     for user in recent_users:
#         username = user['username'] if user['username'] != 'NULL' else 'No username'
#         email = user['email']
#         date = user['date_joined']
#         print(f"Date: {date} | Username: {username} | Email: {email}")


def get_time_of_day(current_time: str) -> str:
    # Extract the hour from the time string
    hour = int(current_time.split(":")[0])

    # Determine the time of day
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"
    
def list_to_string(list_item: list) -> str:
    if not list_item: 
        return ""
    
    if len(list_item) == 1:  
        return list_item[0]
    
    if len(list_item) == 2:  
        return f"{list_item[0]} & {list_item[1]}"
    
    # If there are three or more items
    return ", ".join(list_item[:-1]) + f" {random.choice(['&', 'and', 'with'])} " + list_item[-1]



def getDateTime():
	# Getting Date-Time Info
	current_date = dt.date.today()
	current_time = datetime.now().strftime("%H:%M:%S")

	# Date Format: "YYYY-MM-DD"
	formatted_date = current_date.strftime("%Y-%m-%d")
	date = formatted_date
	time = current_time

	return [date, time]

def HTMLBreak(n):
	breaks = ""

	for x in range(int(n)):
		breaks = breaks + "\n<br>"	

	return breaks

def getOppositeTheme(theme):
	if theme == 'light':
		return 'dark'
	else:
		return 'light'

def oppositeCurrency(currency):
	return "NGN" if currency == "$" else "NGN"


def detectDeviceType(theRequest):
	user_agent = theRequest.user_agent.string.lower()

	if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
		device_type = 'Mobile'
	else:
		device_type = 'Desktop'

	return device_type


def get_mime_type(data):
    decoded_data = base64.b64decode(data)
    image_type = imghdr.what(None, h=decoded_data)
    return f'image/{image_type}' if image_type else 'application/pdf'

def getContractCode() -> str:
	return "7208450356"

def getAPIKey() -> str:
	return "MK_TEST_DBQQF0A5P5"

def getSecretKey() -> str:
	return "Z16JHXZY89TXQS8QFF4YJ44HLCS0YHEG"


def sort_posts_by_datetime(posts_data):
    """
    Sort posts by datestamp and timestamp in ascending order
    
    Args:
        posts_data (dict): Dictionary containing post data
        
    Returns:
        dict: Dictionary of posts sorted by date and time
    """
    # Sort items by datestamp and timestamp
    sorted_items = sorted(
        posts_data.items(),
        key=lambda x: (x[1]['datestamp'], x[1]['timestamp']),
        reverse=True
    )
    
    # Convert back to dictionary while maintaining order
    return dict(sorted_items)

# Example usage:
def display_sorted_posts(posts_data):
    """
    Display sorted posts in a readable format
    """
    sorted_posts = sort_posts_by_datetime(posts_data)
    
    for post in sorted_posts:
        print(f"Date: {post['datestamp']} | Time: {post['timestamp']} | Content: {post['content']}")
        
def reversed_dict(the_dict) -> dict:
    the_dict = list(the_dict.values())
    the_dict = the_dict[::-1]

    dict_of_dicts = {}
    for i, d in enumerate(the_dict):
        dict_of_dicts[f"{id_generator.generate_id(13)}"] = d
    
    return dict_of_dicts