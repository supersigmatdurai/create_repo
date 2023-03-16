from app import app,timedelta,generate_password_hash,check_password_hash,jwt
from app import mysqlconnect,Client,request,generateotp,DictCursor,jsonify,make_response
from app import datetime,uuid,wraps,excute_query,requests

app.config['SECRET_KEY']='9f1c3ef22a0f3356b25df8b5dedb482f'


def token_required(f):
    
    
    @wraps(f)
    
    def decorated(*args, **kwargs):
        conn=mysqlconnect()
        cur=conn.cursor()
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:

            # decoding the payload to fetch the stored details
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            
            current_user = ('select user.id,user.number,user.username,user.emailid,user.dob,user.gender,user.additionalnumber,user.proof,user.resume,user.profilepic,user.createddatetime,exp_edu.id,exp_edu.education,exp_edu.experience from {}  where public_id ="{}"'.format("user" ,data['public_id']))
           
            if current_user is None:
                return{"message":"invaild"}
            
                
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

@app.route('/user11', methods =['GET'])
@token_required
def get_all_users(current_user):
    
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    # querying the database
    # for all the entries in it
    cur.execute(current_user)
    myresult = cur.fetchall()
    print(current_user)
    print(myresult)
    # converting the query objects
    # to list of jsons
    output = []
    for user in myresult:
        # appending the user data json
        # to the response list
        print(user)
        output.append({
                        
             'username':myresult[0]['username'],
              
             'emailid':myresult[0]['emailid']

        })
  
    return jsonify({'user_details':myresult})

#otp generate api 

@app.route('/api/sms',methods=['POST'])

def getotpapi():
    
    data=request.get_json() 
    
    account_sid='AC1067a2c1b524dfca3b8367e1855aae22'
    
    auth_token='c414fbd3de3df803542be91cd47e8dd4'
    
    client=Client(account_sid,auth_token)
    
    otp=generateotp()
    print(otp)
    
    body=' send otp is'+" "+str(otp)
    
    message=client.messages.create(
        from_='+12764962635',
        body=body,
        to=data['number']
    )
    # url='http://site.ping4sms.com/sendsms/?token=44581d25b49c6e628eba93e00a7fbc8f&credit=2&sender=PINMSG&message=Dear%20Customer,Welcome%20to%20PING4SMS&number={}&templateid=1207160974794203441'.format("7904681146")
    # # print(client.msg)
    # # su=msg.sid
    # response = requests.get(url)
    # print(response)
    conn=mysqlconnect()
    
    cur=conn.cursor() 
    
    otp_hash =generate_password_hash(str(otp))
    
    # data['password']=password 
    
    data['public_id']=str(uuid.uuid4())
    print(data['public_id'])
    
    req=cur.execute("SELECT * FROM {} WHERE number='{}'".format("user",data['number']))
    user1=cur.fetchall()
    print(user1)
    print(cur.rowcount)
    
    if cur.rowcount > 0:
        print("i am old")
        
        # check database otp
        user="UPDATE {} SET otp = '{}' WHERE number = '{}'".format("user",otp_hash,data['number'])
        
        cur.execute(user)
        
        conn.commit()
        
        return "true"
    
    else:
        print("i am new ")
    
        cur.execute("INSERT INTO user(public_id,number,otp) VALUES('%s ','%s','%s')" %(data['public_id'],data['number'],otp_hash))
        
        conn.commit()
        
        if message.sid:
            return "true"
        else:
            return "false"


# otp vefication 

@app.route('/sms/verification',methods = ['GET','POST'])

def validotp():
    
    data=request.get_json()
    print(data)
    
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()

    cur.execute('select * from {}  where number="{}" ' .format("user",data['number']))
    myresult = cur.fetchall()
    print(myresult)
 
    if check_password_hash(myresult[0]['otp'], data['otp']):
        
        token = jwt.encode({
            
            'public_id': myresult[0]['public_id'],        
            'exp' : datetime.utcnow() + timedelta(minutes = 20) 
        }, app.config['SECRET_KEY'],algorithm="HS256")

        return jsonify({"msg": "Login success", "user_id":myresult[0]['id']})
    
    else:
        
        result = {"msg": "Login fail", "msgid":"0"}
        
        return jsonify(result) 
    
@app.route("/invaild" ,methods=['POST'])

###user location latitude longitude

@app.route("/api/location_update",methods=['put'])
def location_update():
    data=request.get_json()
    print(data)
    user_id=data['user_id']
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    del data['user_id']
   

    for i,j in data.items():
            
        user='UPDATE {} SET {} = "{}" WHERE id = {}'.format("user",i,j,user_id)
        
        cur.execute(user)
              
        conn.commit()
    
    return ("success")

# otp time out activate

@app.route("/invaild" ,methods=['POST'])
def invalid():
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    
    data=request.json['number']
    
    user="UPDATE {} SET otp = 'Dont_fallow' WHERE number = '{}'".format("user",data)
    
    cur.execute(user)
    
    conn.commit()
    
    return jsonify({"otp":"invaild"})


# new otp service activate sample

@app.route('/send_otp', methods=['POST'])
def send_otp():
    number = 7904681146
    otp=generateotp()
    token = '44581d25b49c6e628eba93e00a7fbc8f'
    credit = '2'
    sender = 'PINMSG'
    otp = str(otp)
    message = f'Dear Customer, Your OTP for velai is {otp}'
    template_id = '1207160974794203441'
    
    url = f'http://site.ping4sms.com/sendsms/?token={token}&credit={credit}&sender={sender}&message={message}&number={number}&templateid={template_id}'
    
    response = requests.get(url)
    
    if response.status_code == 200:

        return 'OTP sent successfully'
    else:
        return 'Error sending OTP'
