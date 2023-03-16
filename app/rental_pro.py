from app import app,jsonify,request,sql,mysqlconnect,DictCursor,excute_query,Nominatim

# rental provider info collect

@app.route("/api/rental_pro_info_get",methods=['POST'])
def rental_pro_info_get():
    data=request.get_json()
    user_id=data['user_id']

    conn=mysqlconnect()
    db=sql()
    conn=mysqlconnect()
        
    cur=conn.cursor()
        
    cur.execute("select * from {} where user_id={}".format("rental_provider_info",user_id))
    
    cur.fetchall()
    
    if cur.rowcount==0:

        query='INSERT INTO {} ({}) VALUES {}'.format("rental_provider_info",",".join([i for i in list(data)]),tuple(data.values()))
        
        cur.execute(query)  
        
        conn.commit() 
        return jsonify({"user":"success"})
    else:

        return jsonify({"user":"already login"})
    
  
@app.route("/api/rental_pro_product_post",methods=['POST'])
def rental_pro_product_post():
    data=request.get_json()
    user_id=data['user_id']
    l1=(data['District']+","+data['state']+","+data['country'])

    data['location']=l1
    del data['District']
    del data['state']
    del data['country']
    conn=mysqlconnect()
    
    conn=mysqlconnect()
        
    cur=conn.cursor()
    geolocator = Nominatim(user_agent="velai")

    location = geolocator.geocode(data['location'])

    l1=location.latitude
    l2=location.longitude
    data['latitude']=l1
    data['longitude']=l2
    if data['pic']=="":
        return jsonify({"post":"please upload picture"})
      
    query='INSERT INTO {} ({}) VALUES {}'.format("rent_post",",".join([i for i in list(data)]),tuple(data.values()))
        
    cur.execute(query)  
        
    conn.commit() 
    return jsonify({"post":"success"})   

@app.route("/api/rent_pro_post_show/<int:user_id>",methods=['GET'])
def  rent_pro_post_show(user_id):
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    
    cur.execute("SELECT rent_post.id, rent_post.product_name,rent_post.product_type,rent_post.pic,rent_post.posteddatetime FROM {} WHERE rent_post.user_id={}".format("rent_post",user_id))
    user=cur.fetchall()
    return jsonify({"posts":user}) 
    
    
    
    

@app.route("/api/rented_products",methods=['POST'])
def rented():
    
        
    data=request.get_json()

    conn=mysqlconnect()
        
    cur=conn.cursor()
        
    cur.execute('select * from {} where user_id="{}" and rent_id ="{}"'.format("rented_products",data['user_id'],data['rent_id']))
    myresult=cur.fetchall()

    if cur.rowcount == 0:

        query='INSERT INTO {} ({}) VALUES {}'.format("rented_products",",".join([i for i in list(data)]),tuple(data.values()))

        cur.execute(query)  
            
        conn.commit()  
             
        return jsonify({"rented":"success"})
    else:
        return jsonify({"rented":"success"})
    
    
@app.route("/api/rented_products/<int:user_id>",methods=['get'])

def rented_pro_list(user_id):
    conn=mysqlconnect()
    conn.cursorclass =DictCursor
    cur=conn.cursor()
    cur.execute("SELECT rent_post.id, rent_post.product_name,rent_post.pic,rented_products.renteddatetime FROM {} inner join rented_products on rented_products.user_id=user.id inner join rent_post on rent_post.id=rented_products.rent_id where user.id={}".format("user",user_id))
    rented_list=cur.fetchall()

    return jsonify({"rented":rented_list})

 # rental provider post swipe show get methods
 
@app.route("/api/rent_pro_products/<int:id>",methods=['GET'])

def rent_pro_products(id):
    
    return excute_query("select * from {} where id={}".format("rent_post",id),'select')


        