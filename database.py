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

  with connection.cursor() as cursor:
    sql = "SELECT `NAME` FROM `ANIME_SHOW` WHERE `NAME` = %s"
    cursor.execute(sql, (item['title']['english'],))
    result = cursor.fetchone()
    if (result == None):
      insertsql = "INSERT INTO `ANIME_SHOW` (`NAME`, `DESCRIPTION`, `PIC`, `STUDIO`) VALUES (%s, %s, %s, %s)"
      cursor.execute(insertsql, (item['title']['english'], item['description'], item['coverImage']['medium'], item['studios']['nodes'][0]['name']))
    connection.commit()

  try:  
    with connection.cursor() as cursor:
      sql = "SELECT `NAME` FROM `MANGA` WHERE `NAME` = %s"
      mangaItem = item['relations']['nodes'][0]
      cursor.execute(sql, (mangaItem['title']['english'],))
      result = cursor.fetchone()
      if (result == None):
        insertsql = "INSERT INTO `MANGA` (`NAME`, `DESCRIPTION`, `PIC`, `AUTHOR`) VALUES (%s, %s, %s, %s)"
        MangaAuthor = mangaItem['staff']['nodes'][0]
        mangasql = "SELECT `NAME` FROM `MANGA_AUTHOR` WHERE `NAME` = %s"
        cursor.execute(mangasql, (MangaAuthor['name']['full'],))
        mangaResult = cursor.fetchone()
        if (mangaResult == None):
          mangainsertsql = "INSERT INTO `MANGA_AUTHOR` (`NAME`, `PIC`) VALUES (%s, %s)"
          cursor.execute(mangainsertsql, (MangaAuthor['name']['full'], MangaAuthor['image']['medium']))
          connection.commit()
        cursor.execute(insertsql, (mangaItem['title']['english'], mangaItem['description'], mangaItem['coverImage']['medium'], MangaAuthor['name']['full']))
  except IndexError:
    print("NO MANGA")