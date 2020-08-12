import sys
import os
import boto3
import requests
import base64
import json
import logging
import pymysql


client_id = "866cbf6c89dd4a98b73b9cd7c41b1366"
client_secret = "a3c236d072604a3980b4632d4b5d54fa"

host = "data-engineering-spotify.cbj4vgtnwqms.us-east-2.rds.amazonaws.com"
port = 3306
username = "jwryu87"
database = "production"
password = "Tkekfl!38"


def main():


    try:
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2', endpoint_url='http://dynamodb.ap-northeast-2.amazonaws.com')
        print("success connect to Dynamo")
    except:
        logging.error('could not connect to dynamodb')
        sys.exit(1)

    try:
        conn = pymysql.connect(host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
        print("success connect to RDB")
    except:
        logging.error("could not connect to rds")
        sys.exit(1)

    headers = get_headers(client_id, client_secret)

    print(headers)

    table = dynamodb.Table('top_tracks')

    print(table)

    cursor.execute('SELECT id FROM artists')

    artist_id = '43ZHCT0cAZBISjO8DG9PnE'
    URL = "https://api.spotify.com/v1/artists/{}/top-tracks".format(artist_id)
    print(URL)


    params = {
        'country': 'SE'
    }

    r = requests.get(URL, params=params, headers=headers)

    raw = json.loads(r.text)


    for track in raw['tracks']:

        data = {
            'artist_id': artist_id,
            # 'country': country
        }

        data.update(track)

        table.put_item(
            Item=data
        )



def get_headers(client_id, client_secret):

    endpoint = "https://accounts.spotify.com/api/token"
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret).encode('utf-8')).decode('ascii')

    headers = {
        "Authorization": "Basic {}".format(encoded)
    }

    payload = {
        "grant_type": "client_credentials"
    }

    r = requests.post(endpoint, data=payload, headers=headers)

    access_token = json.loads(r.text)['access_token']

    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }

    return headers


if __name__=='__main__':
    main()