from app import app ,jsonify,DictCursor,request,mysqlconnect,GC,Nominatim


# job provider  post in longtime job

@app.route('/api/long_job_post',methods=['POST'])

def l_poster():
    
    if request.method=="POST":
        
        data=request.get_json()
        print(data)
        if data['jobpic']==None:
            return jsonify({"post":"please enter the pic"})
        geolocator = Nominatim(user_agent="velai")
        print(geolocator)

        location = geolocator.geocode(data['location'])

        l1=location.latitude
        l2=location.longitude
        data['latitude']=l1
        data['longitude']=l2
        
        
        conn=mysqlconnect()
        
        cur=conn.cursor()
        
        query='INSERT INTO {} ({}) VALUES {}'.format("long_job_post",",".join([i for i in list(data)]),tuple(data.values()))
        
        cur.execute(query)  
        
        conn.commit()  
        
        return jsonify({"post":"success"})

    return jsonify({"post":"success"})


######job provider shorttime job  post++++++++++

@app.route('/api/shorttime_job',methods=['POST'])

def s_job():
    
    if request.method=="POST":
        
        data=request.get_json()
        
        if data['pic']==None:
            return jsonify({"post":"please enter the pic"})
        else:
            print("ism shiort ")
            print(data)
            geolocator = Nominatim(user_agent="velai")

            location = geolocator.geocode(data['location'])

            l1=location.latitude
            l2=location.longitude
            data['latitude']=l1
            data['longitude']=l2
            print(l1)
            print(l2)
            print(" added in latitude and longitude")
            print(data)
        
            conn=mysqlconnect()
            
            cur=conn.cursor()
            
            query='INSERT INTO {} ({}) VALUES {}'.format("shorttime_job",",".join([i for i in list(data)]),tuple(data.values()))
            
            cur.execute(query)  
            
            conn.commit()  
            
            
            
            return jsonify({"post":"success"})

        return jsonify({"post":"success"})

#job provider profile info get api
        
@app.route("/api/job_pro_userinfo_details",methods=['POST'])

def pro_user_details():
    
    if request.method=="POST":
        
        data=request.get_json()
        
        
        conn=mysqlconnect()
        
        cur=conn.cursor()
        if data=="":
            return "please fill all details"
        
        elif data['username']=="":return "missing username"
        elif data['emailid']=="":return "missing emailid"
        
        elif data['proof']=="":return "missing proof"
         
        qurey=cur.execute('select * from {} where user_id="{}" '.format("job_provider_info",data['user_id']))
        
        if not qurey:
            
            query='INSERT INTO {} ({}) VALUES {}'.format("job_provider_info",",".join([i for i in list(data)]),tuple(data.values()))

            cur.execute(query)  
            
            conn.commit()  
            
             
            return jsonify("success")
        
        else:
            print("hiii")
             
            return jsonify({"user":"your already exit"})
        


        

        
       

