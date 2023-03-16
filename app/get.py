from app import app,GC,request,mysqlconnect,excute_query,jsonify,sql,DictCursor


@app.route("/api/job_title" , methods=['GET'])

def job_title():
    
    if request.method=="GET":
        
        return excute_query( "select * from {}".format("job_title"),'select')
@app.route("/api/s_job_title" , methods=['GET'])

def short_job_title():
    
    if request.method=="GET":
        
        return excute_query( "select * from {}".format("short_job_title"),'select')

#  long and short time job like details============

@app.route("/api/s_l_like_job/<string:user_id>",methods=['GET'])
def s_l_like(user_id):
    db=sql()
    conn=mysqlconnect()

    db.execute("select job_provider_info.username,shorttime_job.posteddatetime,shorttime_job.is_short,shorttime_job.latitude,shorttime_job.longitude,shorttime_job.id as short_id,shorttime_job.id ,shorttime_job.job_title,shorttime_job.distance,shorttime_job.Salary,shorttime_job.location,shorttime_job.per,shorttime_job.Duration from {} inner join job_provider_info on job_provider_info.user_id=user.id RIGHT join shorttime_job ON shorttime_job.user_id=user.id inner join s_like_job on shorttime_job.id=s_like_job.s_id where s_like_job.user_id='{}' ORDER by s_like_job.like_datetime DESC".format("user",user_id))
    
    l_job = db.fetchall()
    
    l_job_dis=list(l_job)
        
    db.execute('select latitude,longitude from user where id={}'.format(user_id))
    
    user_la_lo = db.fetchone()
    
    user_location=(user_la_lo['latitude'],user_la_lo['longitude'])
    
    location_job_check=[]
    
    for i in l_job_dis:
        
        New_York = (i['latitude'],i['longitude'])
        
        ss= round(GC((New_York), user_location).km)
        sss=round(ss,1)
        
        i['distance']=sss
        del i['latitude']
        del i['longitude']
        
        location_job_check.append(i)
        
    db.execute("select job_provider_info.username,long_job_post.id,long_job_post.id as long_id ,long_job_post.posteddatetime,long_job_post.latitude,long_job_post.longitude,long_job_post.is_short,long_job_post.job_title,long_job_post.distance,long_job_post.Salary,long_job_post.location,long_job_post.per,long_job_post.email,long_job_post.Duration as time from {} inner join job_provider_info on job_provider_info.user_id=user.id RIGHT join long_job_post ON long_job_post.user_id=user.id inner join l_like_job on long_job_post.id=l_like_job.l_id where l_like_job.user_id = '{}' ORDER by l_like_job.apply_datetime DESC ".format("user",user_id))
    
    l_job = db.fetchall()
    
    l_job_dis=list(l_job)
    
    location_job=[]
    
    for i in l_job_dis:
        
        New_York = (i['latitude'],i['longitude'])
        
        ss= GC((New_York), user_location).km
        sss=round(ss,1)
        i['distance']=sss
        del i['latitude']
        del i['longitude']
        
        location_job.append(i)
    result=list(location_job_check)+list(location_job)

    s=1
    for i in result:
        i['unique_id']=s
        s+=1
    
    return jsonify({"liked_job": sorted(result, key=lambda i: i['posteddatetime'],reverse=True)})


##///// long and short time job apply details /////

@app.route("/api/s_apply_details/<int:user_id>",methods=['GET'])

def s_job_apply_details(user_id):
    db=sql()
    
    conn=mysqlconnect()

    db.execute('select job_provider_info.username,shorttime_job.is_short,shorttime_job.latitude,shorttime_job.longitude,shorttime_job.id as short_id,shorttime_job.job_title,shorttime_job.distance,shorttime_job.Salary,shorttime_job.location,shorttime_job.per,shorttime_job.Duration from {} LEFT join job_provider_info on job_provider_info.user_id=user.id RIGHT join shorttime_job ON shorttime_job.user_id=user.id inner join s_job_apply on shorttime_job.id=s_job_apply.s_p_id where s_job_apply.user_id={}'.format("user",user_id))

    
    l_job = db.fetchall()
    
    l_job_dis=list(l_job)
    print("iam up")
    print(l_job_dis)
        
    db.execute('select latitude,longitude from user where id={}'.format(user_id))
    
    user_la_lo = db.fetchone()
    
    user_location=(user_la_lo['latitude'],user_la_lo['longitude'])
    distance_s=[]
    
    for i in l_job_dis:
        
        New_York = (i['latitude'],i['longitude'])
  
        ss= GC((New_York), user_location).km
        sss=round(ss,1)
        i['distance']=sss
        distance_s.append(i)
        
    db.execute('select job_provider_info.username,long_job_post.latitude,long_job_post.longitude,long_job_post.is_short,long_job_post.id as long_id,long_job_post.job_title,long_job_post.distance,long_job_post.Salary,long_job_post.location,long_job_post.per,long_job_post.Duration as time from {} inner join job_provider_info on job_provider_info.user_id=user.id RIGHT join long_job_post ON long_job_post.user_id=user.id inner join l_job_apply on long_job_post.id=l_job_apply.l_p_id where l_job_apply.user_id={}'.format("user",user_id))
    
    l_job = db.fetchall()
    
    l_job_dis=list(l_job)
    distance_l=[]
    
    for i in l_job_dis:
        
        New_York = (i['latitude'],i['longitude'])
          
        ss= GC((New_York), user_location).km
        sss=round(ss,1)
        i['distance']=sss
        distance_l.append(i)
        
    result=list(distance_s)+list(distance_l)
    s=1
    for i in result:
        i['unique_id']=s
        s+=1
    print("today")    
    print(result)
    
    return jsonify({"s_job_apply_details": sorted(result, key=lambda i: i['distance'])})


@app.route("/api/job_ti_find/<string:location>",methods=['GET'])
def job_scr_(location):
    
    
    return  (excute_query("SELECT * FROM {} where job_title like'%{}%' ".format("shorttime_job",location),'select'))

  ### job_provider all  get methods ============
@app.route("/api/pro_userinfo/<int:user_id>",methods=['GET'])
def pro_info(user_id):
    return excute_query('select job_provider_info.username,job_provider_info.number,job_provider_info.location,job_provider_info.emailid,job_provider_info.gender,job_provider_info.proof,job_provider_info.profilepic,job_provider_info.designation from {} inner join job_provider_info on job_provider_info.user_id=user.id WHERE user_id={}'.format("user",user_id),'select')    
    

@app.route("/api/provide_jobs/<int:user_id>",methods=['GET'])

def provide_job_list(user_id):
    db=sql()
    
    db.execute("select shorttime_job.id as id,shorttime_job.job_title,shorttime_job.is_short,shorttime_job.Salary,shorttime_job.location,shorttime_job.per,shorttime_job.Duration,shorttime_job.isallow_tocall from {} inner join shorttime_job on shorttime_job.user_id=user.id where user.id={}".format("user",user_id))
    short_job=db.fetchall()
    
    db.execute("select COUNT(s_job_apply.user_id)as total_apply,s_job_apply.s_p_id from {} inner join shorttime_job on shorttime_job.user_id=user.id inner join s_job_apply on s_job_apply.s_p_id=shorttime_job.id where shorttime_job.user_id={} GROUP by s_job_apply.s_p_id".format("user",user_id))
    count_apply_myjob=db.fetchall()

    for i in short_job:
        for j in count_apply_myjob:
            if i['id']==j['s_p_id']:
             
                i['count']=j['total_apply']
                
            else:
                pass
        if "count" in i:
            pass
        else:
            i['count']=0
         
    db.execute("select long_job_post.id as id,long_job_post.Duration,long_job_post.per,long_job_post.Education,long_job_post.job_title,long_job_post.location,long_job_post.workspace,long_job_post.Salary,long_job_post.is_short from {} inner join long_job_post on long_job_post.user_id=user.id where user.id={}".format("user",user_id))
    long_job=db.fetchall()
    
    db.execute("select COUNT(l_job_apply.user_id)as total_apply,l_job_apply.l_p_id from {} inner join long_job_post on long_job_post.user_id=user.id inner join l_job_apply on l_job_apply.l_p_id=long_job_post.id where long_job_post.user_id={} GROUP by l_job_apply.l_p_id".format("user",user_id))
    long_apply_cont=db.fetchall()
    for i in long_job:
        for j in long_apply_cont:
  
            if i['id']==j['l_p_id']:

                i['count']=j['total_apply']
               
            
            else:
                pass
        if "count" in i:
            pass
        else:
            i['count']=0
    print(long_job)
                
    return jsonify({"posted_job":list(short_job)+list(long_job)})

@app.route("/api/job_s_apply_user/<int:id>",methods=['GET'])
def job_apply_short_findid(id):

    db=sql()
    db.execute("select job_seeker_info.user_id as id, job_seeker_info.number,job_seeker_info.username,job_seeker_info.emailid,job_seeker_info.resume from {} RIGHT join job_seeker_info on job_seeker_info.user_id=user.id right join s_job_apply on s_job_apply.user_id=job_seeker_info.user_id LEFT join shorttime_job on shorttime_job.id=s_job_apply.s_p_id where s_job_apply.s_p_id={}".format("user",id))
    user=db.fetchall()

    return jsonify({"user":user})

@app.route("/api/job_l_apply_user/<int:id>",methods=['GET'])
def job_apply_long_findid(id):
    db=sql()
    db.execute("select job_seeker_info.user_id as id,job_seeker_info.number,job_seeker_info.username,job_seeker_info.emailid,job_seeker_info.resume from {}  RIGHT join job_seeker_info on job_seeker_info.user_id=user.id right join l_job_apply on l_job_apply.user_id=job_seeker_info.user_id LEFT join long_job_post on long_job_post.id=l_job_apply.l_p_id where l_job_apply.l_p_id={}".format("user",id))
    user=db.fetchall()
    
    return jsonify({"user":user})

@app.route("/api/job_user_apply_list/<int:user_id>",methods=['GET'])

def provide_job_apply_user_list(user_id):
    
    db=sql()
    
    db.execute("select job_seeker_info.username,job_seeker_info.profilepic,shorttime_job.job_title,shorttime_job.is_short,s_job_apply.apply_datetime,s_job_apply.s_p_id as short_id from {} RIGHT join shorttime_job ON shorttime_job.user_id=user.id RIGHT join s_job_apply on shorttime_job.id=s_job_apply.s_p_id left join job_seeker_info on job_seeker_info.user_id=s_job_apply.user_id where user.id={} ORDER BY s_job_apply.apply_datetime DESC".format("user",user_id))
    short_job_apply=db.fetchall()
    db.execute("select job_seeker_info.username,job_seeker_info.profilepic,long_job_post.job_title,long_job_post.is_short,l_job_apply.apply_datetime,l_job_apply.l_p_id as long_id from {} RIGHT join long_job_post ON long_job_post.user_id=user.id RIGHT join l_job_apply on long_job_post.id=l_job_apply.l_p_id left join job_seeker_info on job_seeker_info.user_id=l_job_apply.user_id where user.id={} ORDER BY l_job_apply.apply_datetime DESC".format("user",user_id))
    long_job_apply=db.fetchall()

    return jsonify({"posted_job":list(short_job_apply)+list(long_job_apply)})



@app.route("/api/job_fillter",methods=['POST'])
def job_fillter():
    data= request.get_json()

    s=data['states']
    state=s.replace(" ", "")
    
    location=data['district']+","+state

    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    
    db=sql()
    
    cur.execute("SELECT * FROM {} where location like '%{}%' or location like '%{}%' or job_title like '%{}%' or duration like '%{}%' or Salary like '%{}%'  ".format("shorttime_job",data['district'],state,data['job_title'],data['duration'],data['salary']))

    jobs = cur.fetchall()

    l_job_dis=list(jobs)
        
    db.execute('select latitude,longitude from {} where id={}'.format("user",data['user_id']))
    
    user_la_lo = db.fetchone()
    print(user_la_lo)
    
    user_loc=(user_la_lo['latitude'],user_la_lo['longitude'])
    
    location_job=[]
    
    for i in l_job_dis:
        
        New_York = (i['latitude'],i['longitude'])
        
        ss= GC((New_York), user_loc).km
        sss=round(ss,1)

        i['distance']=sss
     
        location_job.append(i) 
    
    return jsonify({"jobs":location_job}) 


@app.route("/api/like_apply_slideshow",methods=['POST'])
def like_apply_slideshow():
    data=request.get_json()

    conn=mysqlconnect()
    
    conn.cursorclass =DictCursor
    
    cur=conn.cursor()
    if data['table_name']=='shorttime_job':
    
        cur.execute("SELECT job_provider_info.username,job_provider_info.profilepic,shorttime_job.id,shorttime_job.job_title,shorttime_job.Salary,shorttime_job.location,shorttime_job.per,shorttime_job.pic,shorttime_job.description,shorttime_job.latitude,shorttime_job.longitude,shorttime_job.distance,shorttime_job.apply FROM user inner join job_provider_info on job_provider_info.user_id=user.id inner join shorttime_job on shorttime_job.user_id=user.id WHERE shorttime_job.id={}".format(data['post_id']))
                
        result_=cur.fetchall()
            #  job to user location distance calculate#   
        cur.execute('select latitude,longitude from {} where id={}'.format("user",data['user_id']))
            
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
        return jsonify({"post":location_job})
    else:
        cur.execute("SELECT job_provider_info.username,job_provider_info.companyname,job_provider_info.profilepic ,long_job_post.id,long_job_post.job_title,long_job_post.Salary,long_job_post.Duration,long_job_post.location,long_job_post.per,long_job_post.jobpic as pic,long_job_post.workspace,long_job_post.job_description as description,long_job_post.latitude,long_job_post.longitude,long_job_post.distance,long_job_post.apply FROM user inner join job_provider_info on job_provider_info.user_id=user.id inner join long_job_post on long_job_post.user_id=user.id WHERE long_job_post.id={}".format(data['post_id']))
                
        result_=cur.fetchall()
            #  job to user location distance calculate#   
        cur.execute('select latitude,longitude from {} where id={}'.format("user",data['user_id']))
            
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
        return jsonify({"post":location_job})
        
    
    
    
    
        
    
    
    


