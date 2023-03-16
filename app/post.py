from app import app ,jsonify,DictCursor,request,mysqlconnect,GC,sql

# job seeker details inserted api

@app.route("/api/seeker_userinfo_details",methods=['POST'])

def seeker_user_details():
    
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
            
            
            return jsonify({"user":"your already exit"})
        
# jobseeker long time job apply api


@app.route("/api/longtime_apply_job",methods=['POST'])

def longtime_job_apply():
    
    if request.method=="POST":
        
        data=request.get_json()
        
        conn=mysqlconnect()
        
        cur=conn.cursor()
        
        cur.execute('select * from {} where user_id="{}" and l_p_id ="{}"'.format("l_job_apply",data['user_id'],data['l_p_id']))
        
        user=cur.fetchall()
        
        if cur.rowcount ==0:
            
            query='INSERT INTO {} ({}) VALUES {}'.format("l_job_apply",",".join([i for i in list(data)]),tuple(data.values()))

            cur.execute(query)  
            
            conn.commit()  
            
            return jsonify("success")
        
        else:
            
            return jsonify({"user":"your already appied this job"})
        
# jobseeker short time job apply api
        
@app.route("/api/shorttime_apply_job",methods=['POST'])

def shorttime_job_apply(): 
    
    if request.method=="POST":
        
        data=request.get_json()
        
        conn=mysqlconnect()
        
        cur=conn.cursor()
        
        cur.execute('select * from {} where user_id="{}" and s_p_id ="{}"'.format("s_job_apply",data['user_id'],data['s_p_id']))
        user=cur.fetchall()
        
        if cur.rowcount ==0:
            
            query='INSERT INTO {} ({}) VALUES {}'.format("s_job_apply",",".join([i for i in list(data)]),tuple(data.values()))

            cur.execute(query)  
            
            conn.commit()  
             
            return jsonify("success")
        
        else:
            
            return jsonify({"user":"your already appied this job"})
        
# jobn seeker short time job like api
        
@app.route("/api/s_like_details",methods=['POST'])

def s_like():
        
    data=request.get_json()
    
    conn=mysqlconnect()
        
    cur=conn.cursor()
        
    cur.execute('select * from {} where user_id="{}" and s_id ="{}"'.format("s_like_job",data['user_id'],data['s_id']))
    myresult=cur.fetchall()
    
    if cur.rowcount == 0:
            
        query='INSERT INTO {} ({}) VALUES {}'.format("s_like_job",",".join([i for i in list(data)]),tuple(data.values()))

        cur.execute(query)  
            
        conn.commit()  
  
        return jsonify("liked")
        
    else:
        cur.execute('DELETE  FROM {} WHERE user_id={} and s_id={}'.format("s_like_job",data['user_id'],data['s_id']))
        conn.commit()  

        return jsonify("unliked")

# jobn seeker long time job like api

    
@app.route("/api/l_like_job",methods=['POST'])

def l_like():
    
        
    data=request.get_json()
    conn=mysqlconnect()
        
    cur=conn.cursor()
        
    cur.execute('select * from {} where user_id="{}" and l_id ="{}"'.format("l_like_job",data['user_id'],data['l_id']))
    myresult=cur.fetchone()
        
    if cur.rowcount == 0:
            
        query='INSERT INTO {} ({}) VALUES {}'.format("l_like_job",",".join([i for i in list(data)]),tuple(data.values()))

        cur.execute(query)  
            
        conn.commit()  
             
        return jsonify('liked')
        
    else:
            
        cur.execute('DELETE  FROM {} WHERE user_id={} and l_id={}'.format("l_like_job",data['user_id'],data['l_id']))
        conn.commit()  
       
        return jsonify("unliked")
        
 ##################3
 
# long time  job like and apply
        
@app.route("/api/limit/L_like_apply_check/<string:user_id>",methods=['POST'])

def l_aplly_like_check(user_id):
    data=request.get_json()

    page=data['page']*10
    
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    fillter=data['filter']
    
    if fillter['states']=='$' and fillter['district']=='$' and fillter['job_title']=='$' and fillter['duration']=='$' and fillter['salary']=='$':

        cur.execute('SELECT long_job_post.id,job_provider_info.emailid,job_provider_info.companyname,job_provider_info.username,job_provider_info.number,user.number,job_provider_info.profilepic,long_job_post.distance,long_job_post.latitude,long_job_post.longitude,long_job_post.is_short,long_job_post.Salary,long_job_post.isallow_tocall,long_job_post.liked,long_job_post.per,long_job_post.apply,long_job_post.Duration,long_job_post.Education,long_job_post.job_description,long_job_post.job_title,long_job_post.jobpic,long_job_post.location,long_job_post.workspace,long_job_post.mobile_number,long_job_post.email,long_job_post.posteddatetime from {} inner join job_provider_info on job_provider_info.user_id=user.id right join long_job_post on user.id=long_job_post.user_id  limit {},10 '.format("user",page))
            
        l_resultend=cur.fetchall()
        result_=list(l_resultend) 

        cur.execute('select * from {} where user_id={}'.format("l_like_job",user_id))
        my0=cur.fetchall()
    
        if cur.rowcount> 0:


            cur.execute('select l_id from {} where user_id="{}"'.format("l_like_job",user_id))
        
            myresult1=cur.fetchall()
        
            apply=myresult1
    
            for i in result_:
                for j in apply:
                    if i['id']==j['l_id']:
                        i['liked']="true"
                    # job.append(i)
                    else:
                        pass
                if i['liked']=="true":
                    pass
                else:
                    i['liked']="false"
                                
        else:
            for i in result_:
                i['liked']="false"
                    
        ###########ends 
        
        cur.execute('select * from {} where user_id={}'.format("l_job_apply",user_id))
        
        my10=cur.fetchall()
        
        if cur.rowcount> 0:
        
            cur.execute('select l_p_id from {} where user_id="{}"'.format("l_job_apply",user_id))
        
            myresult1=cur.fetchall()
        
            apply=myresult1
    
            for i in result_:
                for j in apply:
                    if i['id']==j['l_p_id']:
                        i['apply']="True"
            
                    else:
                        pass
                if i['apply']=="True":
                    pass
                else:
                    i['apply']="False"
                    
                
        else:
            for i in result_:
                i['apply']="False"     
    
        #  job to user location distance calculate#   
        cur.execute('select latitude,longitude from {} where id={}'.format("user",user_id))
        
        user_la_lo = cur.fetchone()
        
        user_loc=(user_la_lo['latitude'],user_la_lo['longitude'])
        
        location_job=[]
    
        for i in result_:
        
            New_York = (i['latitude'],i['longitude'])
        
            ss= GC((New_York), user_loc).km
            sss=round(ss,1)
            i['distance']=sss
            del i['latitude']
            del i['longitude']
        
            location_job.append(i)
        
        print(result_) 
        return jsonify({"long":sorted(result_, key=lambda i: i['distance'])})
    else:

        db=sql()
        s=fillter['states']
        state=s.replace(" ", "")

        cur.execute("SELECT * FROM {} where location like '%{}%' or location like '%{}%' or job_title like '%{}%' or Duration like '%{}%' or Salary like '%{}%'  ".format("long_job_post",fillter['district'],state,fillter['job_title'],fillter['duration'],fillter['salary']))

        jobs = cur.fetchall()

        l_job_dis=list(jobs)
            
        db.execute('select latitude,longitude from {} where id={}'.format("user",user_id))
        
        user_la_lo = db.fetchone()
        
        user_loc=(user_la_lo['latitude'],user_la_lo['longitude'])
        
        location_job=[]

        
        for i in l_job_dis:
            
            New_York = (i['latitude'],i['longitude'])
                
            Texas = (user_loc) 
            
            ss= GC((New_York), Texas).km
            sss=round(ss,1)

            i['distance']=sss
        
            location_job.append(i) 
            
        
        return jsonify({"long":location_job}) 
    

# long limit ends =================

@app.route("/api/limit/s_like_apply_check/<string:user_id>",methods=['POST'])

def s_aplly_like_check(user_id):
    data=request.get_json()
    
    page=data['page']*10
   
    fillter=data['filter']
    
    
    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    #### filter check return////////////////////
    if fillter['states']=='$' and fillter['district']=='$' and fillter['job_title']=='$' and fillter['duration']=='$' and fillter['salary']=='$':
   
    ########filter in ends////////////////////
    
        cur.execute('select job_provider_info.username,job_provider_info.emailid,job_provider_info.companyname,job_provider_info.profilepic,job_provider_info.number,user.number,shorttime_job.is_short,shorttime_job.distance,shorttime_job.id,shorttime_job.liked,shorttime_job.job_description,shorttime_job.job_title,shorttime_job.Salary,shorttime_job.location,shorttime_job.per,shorttime_job.pic,shorttime_job.Duration,shorttime_job.isallow_tocall,shorttime_job.latitude,shorttime_job.longitude,shorttime_job.apply,shorttime_job.posteddatetime from {} inner join job_provider_info on job_provider_info.user_id=user.id right join shorttime_job on user.id=shorttime_job.user_id  limit {},10'.format("user",page))
        resultend=cur.fetchall()
        result_=list(resultend) 

        cur.execute('select * from {} where user_id={}'.format("s_like_job",user_id))
        my0=cur.fetchall()
    
        if cur.rowcount> 0:


            cur.execute('select s_id from {} where user_id="{}"'.format("s_like_job",user_id))
        
            myresult1=cur.fetchall()
        
            apply=myresult1
    
            for i in result_:
                for j in apply:
                    if i['id']==j['s_id']:
                        i['liked']="true"
                    # job.append(i)
                    else:
                        pass
                if i['liked']=="true":
                    pass
                else:
                    i['liked']="false"
                                
        else:
            for i in result_:
                i['liked']="false"
                    
        ###########ends 
        
        cur.execute('select * from {} where user_id={}'.format("s_job_apply",user_id))
        
        my10=cur.fetchall()
        
        if cur.rowcount> 0:
        
            cur.execute('select s_p_id from {} where user_id="{}"'.format("s_job_apply",user_id))
        
            myresult1=cur.fetchall()
        
            apply=myresult1
    
            for i in result_:
                for j in apply:
                    if i['id']==j['s_p_id']:
                        i['apply']="True"
            
                    else:
                        pass
                if i['apply']=="True":
                    pass
                else:
                    i['apply']="False"
                    
                
        else:
            for i in result_:
                i['apply']="False"     
    
        #  job to user location distance calculate#   
        cur.execute('select latitude,longitude from {} where id={}'.format("user",user_id))
        
        user_la_lo = cur.fetchone()
        
        user_loc=(user_la_lo['latitude'],user_la_lo['longitude'])
        
        location_job=[]
    
        for i in result_:
        
            New_York = (i['latitude'],i['longitude'])
        
            ss= GC((New_York), user_loc).km
            sss=round(ss,1)
            i['distance']=sss
            del i['latitude']
            del i['longitude']
        
            location_job.append(i)
        

        return jsonify({"short":sorted(result_, key=lambda i: i['distance'])})
        
        

    else:

        db=sql()
        s=fillter['states']
        state=s.replace(" ", "")
    
        location=fillter['district']+","+state
    
        user=("SELECT * FROM {} where location like '%{}%' or location like '%{}%' or job_title like '%{}%' or Duration like '%{}%' or Salary like '%{}%'  ".format("shorttime_job",fillter['district'],state,fillter['job_title'],fillter['duration'],fillter['salary']))

        cur.execute(user)
        jobs = cur.fetchall()

        l_job_dis=list(jobs)
            
        db.execute('select latitude,longitude from {} where id={}'.format("user",user_id))
        
        user_la_lo = db.fetchone()
        
        user_loc=(user_la_lo['latitude'],user_la_lo['longitude'])
        
        location_job=[]
        
        
        for i in l_job_dis:
            
            New_York = (i['latitude'],i['longitude'])
                
            Texas = (user_loc) 
            
            ss= GC((New_York), Texas).km
            sss=round(ss,1)

            i['distance']=sss
        
            location_job.append(i) 
        
        return jsonify({"short":location_job}) 
            
        
    


#   short limit ends =================