from app import app ,jsonify,DictCursor,request,mysqlconnect,json,sql

# all user profile show api

@app.route("/api/profile_details_show",methods=['POST'])
def profile_details():
    data=request.get_json()
    print("hiii")
    print(data)

    db=sql()
    
    db.execute('select * from {} where user_id={}'.format(data['userType'],data['user_id']))
    
    user1=db.fetchall()
    
    if db.rowcount>0:
        print(user1)
   
        return jsonify({"profile_info":user1})
    else:
        return jsonify({"profile_info":user1})





