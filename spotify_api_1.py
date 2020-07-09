import sys
import requests
import base64
import json
import logging

client_id = "866cbf6c89dd4a98b73b9cd7c41b1366"
client_secret = "a3c236d072604a3980b4632d4b5d54fa"


def main():

    headers = get_headers(client_id, client_secret)

    ## Spotify Search API
    params = {
        "q": "BTS",
        "type": "artist",
        "limit": "5"
    }


    r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)

    print(r.status_code)
    print(r.text)
    print(r.headers)
    sys.exit(0)



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

    # print(r.status_code)
    # print(r.text)
    # print(type(r.text))
    # print(access_token)
    # print(type(access_token))
    # sys.exit(0)

    headers = {
        "Authorization": "Bearer {}".format(access_token)
    }

    return headers




if __name__=='__main__':
    main()
