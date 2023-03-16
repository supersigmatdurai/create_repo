from app import app ,jsonify,excute_query,mysqlconnect,DictCursor,request,sql,GC


@app.route("/api/rent_post_fillter/<string:product_type>",methods=['get'])
def rent_collection_fillter(product_type):
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    
    cur.execute("select * from {} where product_type like '%{}%'".format("rent_post",product_type))
    my_post=cur.fetchall()
    return jsonify({"rent":my_post})

@app.route("/api/rentsee_choice",methods=['post'])
def choice_rend():
    
    data=request.get_json()
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    cur.execute("SELECT rental_provider_info.username,rent_post.id,rent_post.product_name,rent_post.liked,rent_post.product_type,rent_post.product_fees,rent_post.product_fees_hour,rent_post.product_description,rent_post.pic,rent_post.number,rent_post.address,rent_post.location,rent_post.latitude,rent_post.longitude,rent_post.posteddatetime,rent_post.Duration2,rent_post.Duration FROM {} inner join rental_provider_info on rental_provider_info.user_id=user.id right join rent_post on rent_post.user_id=user.id where rent_post.id>={} and rent_post.product_type like '%{}%' ".format("user",data['post_id'],data['selectedTools']))
    
    user=cur.fetchall()
    result_=list(user)

    cur.execute('select * from {} where user_id={}'.format("rent_see_like",data['user_id']))
    my0=cur.fetchall()
    
    if cur.rowcount> 0:

        cur.execute('select c_h_id from {} where user_id="{}"'.format("rent_see_like",data['user_id']))
        
        myresult1=cur.fetchall()
        
        apply=myresult1

    
        for i in result_:
            for j in apply:
                if i['id']==j['c_h_id']:
                    i['liked']="true"

                else:
                    pass
            if i['liked']=="true":
                pass
            else:
                print("oooooo")
                i['liked']="false"
                                
    else:
        for i in result_:
            i['liked']="false"

    
    
    cur.execute('select latitude,longitude from user where id={}'.format(data['user_id']))
    
    user_la_lo = cur.fetchone()
    
    user_location=(user_la_lo['latitude'],user_la_lo['longitude'])
    
    location_job_check=[]
    
    for i in result_:
        
        New_York = (i['latitude'],i['longitude'])
        
        ss= round(GC((New_York), user_location).km)
        sss=round(ss,1)
        
        i['distance']=sss
        del i['latitude']
        del i['longitude']
        
        location_job_check.append(i)

    
    return jsonify({"choice":location_job_check})

@app.route("/api/rental_see_userinfo_details",methods=['POST'])

def see_user1_details():
    
    if request.method=="POST":
        
        data=request.get_json()
        print("neeeee")
        print(data)

        conn=mysqlconnect()
        
        cur=conn.cursor()
    
        qurey=cur.execute('select * from {} where user_id="{}" '.format("rental_seeker_info",data['user_id']))
        
        if not qurey:
            print("i am old user")
            
            query='INSERT INTO {} ({}) VALUES {}'.format("rental_seeker_info",",".join([i for i in list(data)]),tuple(data.values()))

            cur.execute(query)  
            
            conn.commit()  
            
            
            return jsonify("success")
        
        else:
            print("user already")
             
            return jsonify("already exits")
        
@app.route("/api/rental_call_history",methods=['POST'])

def rental_call_history():
    
    if request.method=="POST":
        
        data=request.get_json()       
        
        conn=mysqlconnect()
        
        cur=conn.cursor()
        
        cur.execute('select * from {} where user_id="{}" and c_h_id ="{}"'.format("rent_see_like",data['user_id'],data['c_h_id']))
        
        user=cur.fetchall()
        
        if cur.rowcount ==0:
            
            query='INSERT INTO {} ({}) VALUES {}'.format("rent_see_like",",".join([i for i in list(data)]),tuple(data.values()))

            cur.execute(query)  
            
            conn.commit()  

            return jsonify("success")
        
        else:
            
            cur.execute('DELETE  FROM {} WHERE user_id={} and c_h_id={}'.format("rent_see_like",data['user_id'],data['c_h_id']))
            conn.commit()  

            return jsonify("unliked")
        
@app.route("/api/rental_see_call_history/<int:user_id>",methods=['GET'])
def rental_see_call_history(user_id):
    conn=mysqlconnect()
        
    cur=conn.cursor()
    
    return excute_query("select rental_provider_info.username,rent_post.id,rent_post.product_name,rent_post.liked,rent_post.product_fees,rent_post.product_fees_hour,rent_post.pic,rent_post.Duration2,rent_post.Duration,rent_post.location FROM {} inner join rental_provider_info on rental_provider_info.user_id=user.id inner join rent_see_like on rent_see_like.user_id=user.id inner join rent_post on rent_post.id=rent_see_like.c_h_id where rent_see_like.user_id={} ORDER by rent_see_like.applydatetime DESC".format("user",user_id),"select")
        

