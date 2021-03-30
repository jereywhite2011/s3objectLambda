########################################################
## populate-tag.py - Populates tags when object is
##         added to S3
########################################################
## Author: Jeremiah White
## License: MIT License
## Credits: Greg Heywood (heywoodonline.com)
## Version: 1.0.1
## Email: jeremiah.white@gmail.com
########################################################


import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
tagValue = "REDACT_AND_TOKENIZE"
tagName = "PROTECTION"


def lambda_handler(event, context):
    print("Recevied event: " + json.dumps(event, indent=2))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        response = s3.put_object_tagging(
            Bucket=bucket,
            Key=key,
            Tagging={
                'TagSet': [
                    {
                        'Key': tagName,
                        'Value': tagValue
                    },
                ]
            }
        )
    except Exception as e:
        print(e)
        print('Error applying tag {} to {}.'.format(tagName, key))
        raise e
