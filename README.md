# Weebdb Populator

This populates the database described in [CS470-Group4/DATABASE](https://github.com/CS470-Group4/DATABASE). It gets the ~1000 most popular anime TV shows and 1000 most popular anime films, and related character, cast, staff and manga information.

Information is provided courtesy of the Anilist.com API. 

## How do I use it?

First, set up the database according to the above schema. For example, run mysql to create the schema:

`mysql -u alice -p`

```
create schema weebdb;
quit;
```

Then `mysql -u alice weebdb < ./DATABASE.sql -p`

The script runs on Python 3, make sure you have that installed. Relevant modules are listed in the `requirements.txt` file and can be installed with

`pip install -r requirements.txt`

The script expects three environment variables to be set, and won't run without them:

```
WEEB_DB_USERNAME
WEEB_DB_PASSWD
WEEB_DBNAME
```

Which are your SQL server username, password, and the name of the database you'll be working on, respectively.

Make sure you set them, eg. `export WEEB_DB_USERNAME alice`

After that, you should be good to go. Just run `python database.py`