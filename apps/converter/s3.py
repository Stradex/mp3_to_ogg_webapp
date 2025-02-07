import boto3
import time
import os
from dotenv import load_dotenv
load_dotenv() 

s3_session={}
s3_client={}
s3_bucket=""

def start_s3_connection():
    global s3_session
    global s3_client
    global s3_bucket

    s3_session=boto3.session.Session()
    s3_client=s3_session.client('s3',
    region_name='nyc3',
    endpoint_url=os.getenv('SPACES_ENDPOINT'),
    aws_access_key_id=os.getenv('SPACES_KEY_ID'),
    aws_secret_access_key=os.getenv('SPACES_KEY'))
    s3_bucket = os.getenv('SPACES_BUCKET')

def s3_get_files(dir_prefix):
    global s3_session
    global s3_client
    global s3_bucket

    paginator = s3_client.get_paginator('list_objects')
    s3_results = paginator.paginate(
        Bucket=s3_bucket,
        Prefix=dir_prefix,
        PaginationConfig={'PageSize': 1000}
    )
    bucket_object_list = []
    for page in s3_results:
        if "Contents" in page:
            for key in page["Contents"]:
                s3_file_name = key['Key'].split('/')[-1]
                bucket_object_list.append(s3_file_name)
    return bucket_object_list

def s3_get_uploaded_files():
    return s3_get_files("upload/")

def s3_get_converted_files():
    return s3_get_files("converted/")

def s3_download_file(remote_src, local_dest):
    s3_client.download_file(s3_bucket, remote_src, local_dest)

def s3_upload_file(local_src, remote_dest):
    s3_client.upload_file(local_src, s3_bucket, remote_dest, ExtraArgs={
        'ACL': 'public-read',
        'ContentType': 'audio/mpeg; charset=binary',
    })
