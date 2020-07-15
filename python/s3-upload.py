#!/usr/bin/python3
import boto3
import os.path
import sys
from botocore.exceptions import ClientError
import logging

#When ruuning as a crontab you need to sometimes specify the home directory so the script finds the AWS credentials
#os.environ['HOME'] = "~/"

# destination bucket name
bucket_name = 'somebuckername'
# source directory
sourceDir = '/Users/jay/Desktop/testfiles/'

# destination directory name (on s3), needs a trailing slash
destDir = ''

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, destDir + object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


uploadFileNames = []

for (sourceDir, dirname, filename) in os.walk(sourceDir):
    uploadFileNames.extend(filename)
    break

for filename in uploadFileNames:
    upload_file(sourceDir + filename, bucket_name, filename)

#Deletes files from local system
for filename in uploadFileNames:
    os.system('rm "' + sourceDir  + filename + '"')