from sqlite3 import connect
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

anime_obj = download.get_anime("TV")

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
  
      updateanimesql = "UPDATE `ANIME_SHOW` SET `MANGA_ID` = %s WHERE `NAME` = %s"
      cursor.execute(updateanimesql, (mangaItem['title']['english'], item['title']['english']))
      connection.commit()

  except IndexError:
    print("NO MANGA")

  for character in item['characters']['edges']:
    character_obj = {}
    character_obj['name'] = character['node']['name']['full']
    character_obj['desc'] = character['node']['description']
    character_obj['pic'] = character['node']['image']['medium']
    character_obj['va'] = {}
    try:
      character_obj['va'] = character['voiceActors'][0]
    except IndexError:
      print("No VA")
    character_obj['role'] = character['role']
    if (character_obj['role'] in ['SUPPORTING', 'BACKGROUND']):
      character_obj['role'] = 'SIDE'
    with connection.cursor() as cursor:
      charactersql = "SELECT `NAME` FROM `ANIME_CHARACTER` WHERE `NAME` = %s"
      cursor.execute(charactersql, (character_obj['name']))
      result = cursor.fetchone()
      if (result == None):
        insertcharactersql = "INSERT INTO `ANIME_CHARACTER` (`NAME`, `BIO`, `PIC`, `CHARACTER_TYPE`) VALUES (%s, %s, %s, %s)"
        cursor.execute(insertcharactersql, (character_obj['name'], character_obj['desc'], character_obj['pic'], character_obj['role']))
        connection.commit()
    with connection.cursor() as cursor:
      va_sql = "SELECT `NAME` FROM `VOICE_ACTOR` WHERE `NAME` = %s"
      if (character_obj['va'] != {}):
        cursor.execute(va_sql, (character_obj['va']['name']['full']))
        result = cursor.fetchone()
        if (result == None):
          insertVASQL = "INSERT INTO `VOICE_ACTOR` (`NAME`, `BIO`, `PIC`, `A_SHOW`, `CHARACTER_PLAYED`) VALUES (%s, %s, %s, %s, %s)"
          cursor.execute(insertVASQL, (character_obj['va']['name']['full'], character_obj['va']['description'], character_obj['va']['image']['medium'], item['title']['english'], character_obj['name']))
          connection.commit()

  for staff_member in item['staff']['edges']:
    with connection.cursor() as cursor:
      staff_sql = "SELECT `NAME` FROM `STAFF_MEMBERS` WHERE `NAME` = %s"
      cursor.execute(staff_sql, (staff_member['node']['name']['full']))
      result = cursor.fetchone()
      if (result == None):
        insertStaffSQL = "INSERT INTO `STAFF_MEMBERS` (`NAME`, `BIO`, `ROLE`, `PIC`, `A_SHOW`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insertStaffSQL, (staff_member['node']['name']['full'], staff_member['node']['description'], staff_member['role'], staff_member['node']['image']['medium'], item['title']['english']))
        connection.commit()
    