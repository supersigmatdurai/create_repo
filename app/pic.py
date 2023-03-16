from app import app ,request,jsonify,boto3,emoji

##### aws files or images upload code start ++++++++++++++++++=

BUCKET_NAME='zealzoft31'
s3=boto3.client('s3')
end_point='https://zealzoft31.s3.ap-south-1.amazonaws.com'

@app.route('/api/job_post/aws_upload/<int:user_id>',methods=['POST'])

def upload_aws_poster(user_id): 
    
    file = request.files['file']
    
    s3.put_object(Bucket=BUCKET_NAME, 
                      Key=f'{str(user_id)}/'+file.filename, 
                      Body=file,
                      ContentType='image/*')
    
    result=(f"{end_point}/{str(user_id)}/{file.filename}")
       
    return jsonify({"updated":result,"done":emoji.emojize('Python is :thumbs_up:')})


@app.route('/api/file/aws_upload/<int:user_id>',methods=['POST'])

def upload_aws_poster_file(user_id): 
    
    file = request.files['file']
    
    s3.put_object(Bucket=BUCKET_NAME, 
                      Key=f'{str(user_id)}/'+file.filename, 
                      Body=file,
                      ContentType='file/*')
    
    result=(f"{end_point}/{str(user_id)}/{file.filename}")
       
    return jsonify({"updated":result})
    