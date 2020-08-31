import sys
import os
import boto3
import requests
import base64
import json
import logging
import pymysql

from boto3.dynamodb.conditions import Key, Attr

def main():

    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
    except:
        logging.error('could not connect to dynamodb')
        sys.exit(1)

    table = dynamodb.Table('top_tracks')

    response = table.query(
        # KeyFilter
        FilterExpression=Attr('popularity').gt(50)
    )
    print(response['Items'])



if __name__=='__main__':
    main()