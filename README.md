# s3objectLambda

Below are a few instructions on how to setup this function.

## Upload Lambda Functions
1. Upload the protectInfo and populate-tag lambda functions, per the *.yaml configurations and ./src directories

## Create Bucket and Access Points
2. Create a bucket, an accesspoint for the bucket, and an object lambda access point and assign the bucket-policy.json to the bucket. Add the bucket as a trigger to the populate-tag lambda

## Create Users and Groups
3. Create Groups for redaction and tokenization with the same name as the REDACTION_GROUP and TOKENIZATION_GROUP environment variables in the protectInfo Lambda Function
4. Give the redaction and tokenization groups the AWSLambdaRole and the 'S3 Object Lambda' GetObject permission on the object lambda access point

## Update the Lambda Roles
5. Give the populate-tag role the AmazonS3FullAccess policy
6. Give the protectInfo role the AmazonS3FullAccess, IAMReadOnlyAcces, and AWSLambda_FullAccess policies and the 'S3 Object Lambda' Full access permission

## Test Scripts
* ./test/example_object.json is the freetext example of an object on the bucket
* ./test/get_objects_and_compare.py is a script that will pull an object from the S3 Object Lambda
* ./test/test_tokenization.py is a script that shows the tokenization function and it's inverse for a given string
