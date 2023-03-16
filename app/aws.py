from app import app ,request,jsonify,boto3

##### aws files or images upload code start ++++++++++++++++++=

BUCKET_NAME='zealzoft31'
s3=boto3.client('s3')
end_point1='https://zealzoft31.s3.ap-south-1.amazonaws.com'

@app.route('/api/job_post/aws_upload/<int:user_id>',methods=['POST'])

def upload_aws_poster(user_id): 
    
    file = request.files['file']
    
    s3.put_object(Bucket=BUCKET_NAME, 
                      Key=f'{str(user_id)}/'+file.filename, 
                      Body=file,
                      ContentType='image/png')
    
    result=(f"{end_point1}/{str(user_id)}/{file.filename}")
    
    # user="UPDATE {} SET post_pic = '{}' WHERE post_id = {}".format("job_post",result,post_id)

    # cur.execute(user)
    # conn.commit()
       
    return jsonify({"updated":result})