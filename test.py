import sys
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
        conn = pymysql.connect(host, user=username, passwd=password, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = conn.cursor()
    except:
        logging.error("could not connect to rds")
        sys.exit(1)

    cursor.execute("SHOW TABLES")
    print(cursor.fetchall())

    print("success")
    #
    # query = "INSERT INTO artist_genres (artist_id, genre, updated_at) VALUES ('{1}', '{0}', NOW())".format('1234', 'hip-hop')
    # cursor.execute(query)
    # conn.commit()


    sys.exit(0)

    headers = get_headers(client_id, client_secret)

    ## Spotify Search API
    params = {
        "q": "BTS",
        "type": "artist",
        "limit": "1"
    }

    r = requests.get("https://api.spotify.com/v1/search", params=params, headers=headers)

    raw = json.loads(r.text)
    print(raw['artists'])


    sys.exit(0)





if __name__=='__main__':
    main()
