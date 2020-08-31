# production 데이터 베이스 시작
# create database production;
use production;

show databases;
show tables;

---------------------------------------------------------------------------------------
# people 테이블
create table people (
first_name varchar(20)
,last_name varchar(20)
,age int);

select * from people;

---------------------------------------------------------------------------------------
# artists 테이블
CREATE TABLE artists (
id varchar(255),
name varchar(255),
followers integer,
popularity integer,
url varchar(255),
image_url varchar(255),
 primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table artist add column updated_at timestamp default current_timestamp
on update current_timestamp;

select * from artists;

---------------------------------------------------------------------------------------
# artist_genres 테이블
CREATE TABLE artist_genres (
artist_id varchar(255),
genre varchar(255),
unique key (artist_id, genre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
alter table artist_genres add column country varchar(255);
alter table artist_genres add column updated_at timestamp default current_timestamp
on update current_timestamp;

select * from artist_genres;

---------------------------------------------------------------------------------------
# top_tracks; 테이블
select * from top_tracks;