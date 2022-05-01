import pymysql
import os
import download
import pprint

try:
  db_pw = os.environ['WEEB_DB_PASSWD']
  db_username = os.environ['WEEB_DB_USERNAME']
  db_dbname = os.environ['WEEB_DBNAME']
except KeyError:
  print("Make sure the environment variables are set")

connection = pymysql.connect(host='localhost', user=db_username, password=db_pw, database=db_dbname, cursorclass=pymysql.cursors.DictCursor)

anime_obj = download.get_anime()

for item in anime_obj:
  print(item['title']['english'], item['coverImage']['medium'], item['studios']['nodes'][0]['name'])
  try:  
    print( "MANGA: ", item['relations']['nodes'][0]['title']['english'])
  except IndexError:
    print("NO MANGA")

  with connection.cursor() as cursor:
    sql = "SELECT `NAME` FROM `ANIME_SHOW` WHERE `NAME` = %s"
    cursor.execute(sql, (item['title']['english'],))
    result = cursor.fetchone()
    print(result)
    if (result == None):
      insertsql = "INSERT INTO `ANIME_SHOW` (`NAME`, `DESCRIPTION`, `PIC`, `STUDIO`) VALUES (%s, %s, %s, %s)"
      cursor.execute(insertsql, (item['title']['english'], item['description'], item['coverImage']['medium'], item['studios']['nodes'][0]['name']))
    connection.commit()