create external table if not exists top_tracks(
  id string,
  artists_id string,
  name string,
  popularity int,
  external_url string
) partitioned by (dt string)
stored as parquet location 's3://spotify-artists-rjw/top-tracks/' tblproperties("parquet.compress"="SNAPPY")


MSCK REPAIR table top_tracks



create external table if not exists audio_features(
  id string,
  danceability double,
  energy double,
  key int,
  loudness double,
  mode int,
  speechiness double,
  acousticness double,
  instrumentalness double,
) partitioned by (dt string)
stored as parquet location 's3://spotify-artists-rjw/audio_features/' tblproperties("parquet.compress"="SNAPPY")




MSCK REPAIR table audio_features