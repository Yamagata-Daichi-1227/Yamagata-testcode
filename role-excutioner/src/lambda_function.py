import boto3
import datetime
import time
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    logger.info(str(event))
    if 'detail' in event:
        detail = event['detail']
        if 'configRuleName' in detail:
          # access-keys-rotated
            if detail['configRuleName'] == 'access-keys-rotated':
                iam = boto3.client('iam')
                users = iam.list_users()
                for user in users['Users']:
                    if detail['resourceId'] == user['UserId']:
                        access_keys = iam.list_access_keys(UserName=user['UserName'])
                        for access_key in access_keys['AccessKeyMetadata']:
                            create_date = access_key['CreateDate'].timestamp()
                            now = time.time()
                            if now - create_date > 60*60*24*0:
                                #response = iam.delete_access_key(UserName=user['UserName'],AccessKeyId=access_key['AccessKeyId'])
                                print("notification")