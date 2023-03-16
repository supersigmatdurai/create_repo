from app import app,request,mysqlconnect,DictCursor,jsonify,emoji,sql


# jobseeker  user information posted##################33
@app.route("/api/job_see_userinfo_details",methods=['POST'])

def see_user_details():
    
    if request.method=="POST":
        
        data=request.get_json()
        
        conn=mysqlconnect()
        
        cur=conn.cursor()
    
        qurey=cur.execute('select * from {} where user_id="{}" '.format("job_seeker_info",data['user_id']))
        
        if not qurey:
            
            query='INSERT INTO {} ({}) VALUES {}'.format("job_seeker_info",",".join([i for i in list(data)]),tuple(data.values()))

            cur.execute(query)  
            
            conn.commit()  
            
            return jsonify("success")
        
        else:
             
            return jsonify("already exits")
    
    
# user education insert     
        
@app.route("/api/user/education",methods=['POST'])   
def edu():
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    data= request.get_json()
        
    query='INSERT INTO {} ({}) VALUES {}'.format("education",",".join([i for i in list(data)]),tuple(data.values()))
        
    cur.execute(query)
    conn.commit()
    return jsonify({"user":"success"})
    
# jobseeker experience insert

@app.route("/api/user/experience",methods=['POST'])   
def exe():
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    data= request.get_json()
    
    
    query='INSERT INTO {} ({}) VALUES {}'.format("experience",",".join([i for i in list(data)]),tuple(data.values()))
    
    cur.execute(query)
    conn.commit()
    return jsonify({"user":"success"})

# All user profile info updated 

@app.route("/api/user_details_update/<int:user_id>" ,methods=['PUT'])
def details_up(user_id):
    
    data=request.get_json()
    
    tname=data['userType']

    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    
    del data['userType']

    for i,j in data.items():
            
        user='UPDATE {} SET {} = "{}" WHERE user_id = {}'.format(tname,i,j,user_id)
        
        cur.execute(user)
              
        conn.commit()
            
    cur.execute("select * from {} where user_id={}".format(tname,user_id))
    myreult2=cur.fetchall()
        
    return jsonify({"profile_info":myreult2})

#initilize user profile pic update 

@app.route("/api/prfilepic_update",methods=['PUT'])
def pro_pic():
    
    data=request.get_json()
    
    tname=data['userType']
    user_id=data['user_id']

    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    del data['userType']
    del data['user_id']
    

    for i,j in data.items():
            
        user='UPDATE {} SET {} = "{}" WHERE user_id = {}'.format(tname,i,j,user_id)
        
        cur.execute(user)
              
        conn.commit()
    
    return ("success")

#get all user number api

@app.route("/api/user_number/<int:user_id>",methods=['GET'])
def user_num(user_id):
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    cur.execute('select number from {} where id={}'.format("user",user_id))
    user=cur.fetchone()
    
    return (user)

# jobseeker education  get api

@app.route("/api/education/<int:user_id>",methods=['get'])
def educa(user_id):
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    cur.execute('select * from {} where user_id={}'.format("education",user_id))
    user=cur.fetchall()
    return jsonify({"education":user})

# jobseeker experience  get api

@app.route("/api/experience/<int:user_id>",methods=['get'])
def exep(user_id):
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    cur.execute('select * from {} where user_id={}'.format("experience",user_id))
    user=cur.fetchall()
    return jsonify({"experience":user})

# table type data given 

@app.route("/api/exp_eductaion_re",methods=['post'])
def exp_edu():
    data=request.get_json()

    db=sql()
    db.execute('select *from {} where id={}'.format(data['tableType'],data['id']))
    result=db.fetchall()
    return result
    
@app.route("/api/edu_exp_update",methods=['PUT'])
def edu_exp_update():
    
    data=request.get_json()

    tname=data['tableType']
    user_id=data['id']

    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    del data['tableType']
    del data['id']
    

    for i,j in data.items():
            
        user='UPDATE {} SET {} = "{}" WHERE id = {}'.format(tname,i,j,user_id)
        
        cur.execute(user)
              
        conn.commit()
    
    return jsonify({"user":"success"})   


@app.route("/api/user_in_or_out",methods=['POST'])
def in_or_out():
    data=request.get_json()

    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    
    cur.execute('select * from {} where user_id={}'.format(data['userType'],data['user_id']))
    user=cur.fetchall()

    if cur.rowcount >0:
        
        return  jsonify({"result":True,"userType":data['userType']})
    else:
        return jsonify({"result":False,"userType":data['userType']})

