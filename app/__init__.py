from flask import Flask 
from flask import  Flask,request,jsonify, abort,make_response,session,json
import pymysql
from twilio.rest import Client 
import random
from flask_cors import CORS
import logging as logger
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import geopy
import requests
from geopy.distance import geodesic as GC 
import uuid 
import emoji
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename
from geopy.geocoders import Nominatim

import boto3
from flask_swagger_ui import get_swaggerui_blueprint

print(emoji.emojize('Python is :red_heart:'))



def mysqlconnect(): 
    # To connect MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password = "",
        db='velai',
        )
    return conn
app= Flask (__name__)
CORS(app)
def sql():
    conn=mysqlconnect()
    
    
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    data=cur
    return data
# flask swagger configs
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Velai App"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def excute_query(query,qtype):
    #logger.info("mysql connecting...")
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    logger.info('mysql connect successfully.')
    cur=conn.cursor()
    logger.info(query)
    cur.execute(query)
    if qtype.upper()=="SELECT":
        return jsonify(cur.fetchall())
    else:
        conn.commit()
        return jsonify({"Success":"{} Sucessfully.".format(qtype.lower())})

def generateotp():
    
    return random.randrange(1000,9999)

from app import views
from app import user
from app import post
from app import get
from app import pic
from app import provider_post
from app import profile
from app import rental_pro
from app import rental_seeker
