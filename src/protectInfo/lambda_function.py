########################################################
## lambda_function.py - The driver behind redact/token
########################################################
## Author: Jeremiah White
## License: MIT License
## Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


import boto3
import json
import lambdalogging
from constants import PROTECTED_FIELDS, REDACTION_MODE, REDACTION_GROUP_NAME, \
    TOKENIZATION_GROUP_NAME, CHR_TOKENS, NUM_TOKENS, TOKENIZATION_STRING, \
    TOKENIZATION_INTEGER, CHR_TOKENS_REV, NUM_TOKENS_REV, ROTATION

# Set initial values
redaction = False
tokenization = False

LOG = lambdalogging.getLogger(__name__)


def lambda_handler(event, context):
    # Setup
    LOG.info(event)
    determine_protection(event)
    global rotation = ROTATION

    # Setup S3 client
    object_get_context = event["getObjectContext"]
    request_route = object_get_context["outputRoute"]
    request_token = object_get_context["outputToken"]
    s3 = boto3.client('s3')

    # Get object from S3
    bucket = event["configuration"]["supportingAccessPointArn"]
    key = get_key(event["userRequest"]["url"])
    response = s3.get_object(Bucket=bucket, Key=key)
    original_object = response["Body"].read().decode('utf-8')

    # Get Tags from object
    tagset = get_tagset(s3, bucket, key)
    mode = "UNPROTECTED"
    for tag in tagset:
        if tag["Key"] == "PROTECTION":
            mode = tag["Value"]

    # Transform object with either redaction or tokenization
    if (mode == "REDACT" or mode == "REDACT_AND_TOKENIZE") and redaction:
        transformed_object = redact_data(original_object)
    elif (mode == "TOKENIZE" or mode == "REDACT_AND_TOKENIZE") and tokenization:
        transformed_object = tokenize_data(original_object)
    else:
        transformed_object = original_object
    LOG.info("Object transformed from " + original_object + " to " +
             transformed_object)

    # Write object back to S3 Object Lambda
    s3.write_get_object_response(Body=transformed_object,
                                 RequestRoute=request_route, RequestToken=request_token)
    return {'status_code': 200}


def determine_protection(event):
    # Determine whether to tokenize or redact data
    # Void return
    global redaction
    global tokenization
    iam = boto3.client('iam')

    # Get redaction and tokenization groups
    redaction_group = iam.get_group(GroupName=REDACTION_GROUP_NAME)
    redaction_users = redaction_group["Users"]
    tokenization_group = iam.get_group(GroupName=TOKENIZATION_GROUP_NAME)
    tokenization_users = tokenization_group["Users"]

    # determine whether the user is in either the redact or token group
    for user in redaction_users:
        if event["userIdentity"]["arn"] == user["Arn"]:
            redaction = True
        else:
            redaction = False
    for user in tokenization_users:
        if event["userIdentity"]["arn"] == user["Arn"]:
            tokenization = True
        else:
            tokenization = False


def get_key(object_url):
    # Pulls the object key from the given url
    # Returns the object Key
    key_start = object_url.find("aws.com/") + len("aws.com/")
    key_end = object_url.find("?")
    if key_end == -1:
        key_end = len(object_url)
    return object_url[key_start:key_end]


def get_tagset(s3_client, bucket, key):
    # Pulls tagset from the object in S3
    # Returns the tagset on the object
    return s3_client.get_object_tagging(Bucket=bucket, Key=key)["TagSet"]


def is_json(myjson):
    # Determines whether a value is a json or not
    # Returns a boolean
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def redact_data(data):
    # Redacts Data according to the configuration
    # Returns the redacted data
    if is_json(data):
        json_object = json.loads(data)
        for key in json_object:
            if key in PROTECTED_FIELDS:
                if REDACTION_MODE == 'EXPLICIT':
                    json_object[key] = 'REDACTED'
                elif REDACTION_MODE == 'REPLACE':
                    tmps = json_object[key].split('-')
                    for i in range(len(tmps)):
                        tmps[i] = "*" * len(tmps[i])
                    json_object[key] = "-".join(tmps)
        return json.dumps(json_object)
    return data


def tokenize(input_string):
    # Tokenizes an input string by rotating around a couple dict
    # Returns the tokenized string
    ts_length = len(TOKENIZATION_STRING)
    tokens = []
    for char in input_string:
        if char in TOKENIZATION_STRING:
            rotation = (CHR_TOKENS_REV[char] + rotation) % ts_length
            tokens.append(CHR_TOKENS[rotation])
        elif char in TOKENIZATION_INTEGER:
            rotation = (NUM_TOKENS_REV[char] + rotation) % 10
            tokens.append(NUM_TOKENS[rotation])
        else:
            tokens.append(char)
    return "".join(tokens)


def tokenize_data(data):
    # Takes a json and tokenizes fields per configuration
    # Returns a tokenized json
    if is_json(data):
        json_object = json.loads(data)
        for key in json_object:
            if key in PROTECTED_FIELDS:
                json_object[key] = tokenize(json_object[key])
        return json.dumps(json_object)
    return data
