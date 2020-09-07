import sys
import os
import logging
import boto3
import requests
import base64
import json
import pymysql
from datetime import datetime
import pandas as pd
import jsonpath  # pip3 install jsonpath --user

client_id = "866cbf6c89dd4a98b73b9cd7c41b1366"
client_secret = "a3c236d072604a3980b4632d4b5d54fa"

host = "data-engineering-spotify.cbj4vgtnwqms.us-east-2.rds.amazonaws.com"
port = 3306
username = "jwryu87"
database = "production"
password = "Tkekfl!38"

# top_tracks과 audio_features 를 다 가져와서
# parquet 화 로 변형을 시키고
# S3 의 파티션화된 폴더 안에 데이터를 저장

def main():
    # RDS 접속
    try:
        conn = pymysql.connect(host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("could not connect to rds")
        sys.exit(1)

    headers = get_headers(client_id, client_secret)
########################################################################################################################
    # RDS - 아티스트 ID를 가져오고
    cursor.execute("SELECT id FROM artists LIMIT 10")

    top_track_keys = {
        "id": "id",
        "name": "name",
        "popularity": "popularity",
        "external_url": "external_urls.spotify"
    }
########################################################################################################################
    # API - Top Tracks Spotify 가져오고
    top_tracks = []
    for (id, ) in cursor.fetchall():

        URL = "https://api.spotify.com/v1/artists/{}/top-tracks".format(id) # loop를 돌면서 artists ID 가 들어간 URL을 만든다
        params = {
            'country': 'US'
        }
        r = requests.get(URL, params=params, headers=headers) # API 요청 (params, headers 가 필요함) (headers 는 위에서 define을 했음)
        raw = json.loads(r.text) # 가져온 API json 형식의 데이터를 raw에 저장

        for i in raw['tracks']: # 필요한 것은 raw 의 tracks
            top_track = {}
            for k, v in top_track_keys.items():
                top_track.update({k: jsonpath.jsonpath(i, v)})
                top_track.update({'artist_id': id})
                top_tracks.append(top_track)

    # track_ids
    track_ids = [i['id'][0] for i in top_tracks]

    # (parquet 화 시 struct 에 문제가 있을 수 있다.)
    # parquet 화 과정에서 아래와 유사한 데이터 파이프라인 과정이 필요
    # > s3의 가장 raw 데이터가 들어옴
    # > parquet 화 하고 싶은 몇개의 데이터만 뽑아옴
    # > 이것들만 parquet 화 하여 다시 다른 S3 버킷안에 저장

    top_tracks = pd.DataFrame(top_tracks)
    top_tracks.to_parquet('top-tracks.parquet', engine='pyarrow', compression='snappy') # parquet 화 된것이 더 퍼포먼스가 좋고 압축할떄 더 효율이 있다.

    # 여기까지 parquet 을 통해서 top_tracks은 완성
    ############################################################################################################


    dt = datetime.utcnow().strftime("%Y-%m-%d")

    s3 = boto3.resource('s3')
    object = s3.Object('spotify-artists-rjw', 'top-tracks/dt={}/top-tracks.parquet'.format(dt))
    data = open('top-tracks.parquet', 'rb')
    object.put(Body=data)
    # S3 import



    tracks_batch = [track_ids[i: i+100] for i in range(0, len(track_ids), 100)]

    audio_features = []
    for i in tracks_batch:

        ids = ','.join(i)
        URL = "https://api.spotify.com/v1/audio-features/?ids={}".format(ids)

        r = requests.get(URL, headers=headers)
        raw = json.loads(r.text)

        audio_features.extend(raw['audio_features'])

    audio_features = pd.DataFrame(audio_features)
    audio_features.to_parquet('audio-features.parquet', engine='pyarrow', compression='snappy')




    s3 = boto3.resource('s3')
    object = s3.Object('spotify-artists-rjw', 'audio-features/dt={}/top-tracks.parquet'.format(dt))
    data = open('audio-features.parquet', 'rb')
    object.put(Body=data)



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