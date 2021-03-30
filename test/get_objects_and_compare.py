########################################################
# get_and_compare_objects.py - Test of token and redact
# this checks the permissions of groups and
# demonstrates the redact/token feature
########################################################
# Author: Jeremiah White
# License: MIT License
# Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


import boto3
import botocore

# Declare clients, buckets and access points
s3_redact = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
s3_token = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='')
orig_bucket = 'jeremiah-white-bucket'
access_point = 'arn:aws:s3:us-east-2:587941359663:accesspoint/redact-accesspoint'
lambda_access_point = 'arn:aws:s3-object-lambda:us-east-2:587941359663:accesspoint/test'


def attempt_get(client, bucket):
    # Attempts to get object from bucket or access point
    # Void return
    try:
        data = client.get_object(
            Bucket=bucket,
            Key='example.json')
        print(data['Body'].read().decode('utf-8'))
    except botocore.exceptions.ClientError as err:
        print(err)


# Attempt to access bucket and access points directly as root
print('ROOT PERMISSIONS')
print('+++++++++++++++++')
# Expected access denied
print('Object from the S3 bucket using root permissions')
attempt_get(s3, orig_bucket)
# Expected success with plain text
print('Object from the access point using root permissions')
attempt_get(s3, access_point)
# Expected success with plain text
print('Object from the lambda using root permissions')
attempt_get(s3, lambda_access_point)

# Attempts to reach access points as redact user
print('REDACT PERMISSIONS')
print('+++++++++++++++++')
# Expected access denied
print('Object from the access point using redact permissions')
attempt_get(s3_redact, access_point)
# Expected redacted return
print('Object from the lambda using redact permissions')
attempt_get(s3_redact, lambda_access_point)

# Attempts to reach access points as token user
print('TOKEN PERMISSIONS')
print('+++++++++++++++++')
# Expected access denied
print('Object from the access point using token permissions')
attempt_get(s3_token, access_point)
# Exptected tokenized results
print('Object from the lambda using token permissions')
attempt_get(s3_token, lambda_access_point)
