#!/usr/bin/env python

import os
import praw
import json
import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'scraped'

TABLES = {}
TABLES['showerthoughts'] = (
    "CREATE TABLE `showerthoughts` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `url` varchar(255) NOT NULL,"
    "  `title` varchar(4000) NOT NULL,"
    "  `post_timestamp` timestamp NOT NULL,"
    "  PRIMARY KEY (`id`), UNIQUE KEY `url` (`url`)"
    ") ENGINE=InnoDB")

add_showerthought = ("INSERT INTO showerthoughts "
    "(url, title, post_timestamp) "
    "VALUES (%s, %s, FROM_UNIXTIME(%s))")

def initialize_db():
    connection = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database=DB_NAME)
    print 'connected to mysql'

    cursor = connection.cursor()
    try:
        cursor.execute(TABLES.get('showerthoughts'))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("showerthoughts table already exists")
        else:
            print(err.msg)
    else:
        print("showerthoughts table created")
    return connection, cursor

def main():
    connection, cursor = initialize_db()

    # uses environment variables
    # http://praw.readthedocs.io/en/latest/getting_started/configuration/environment_variables.html
    reddit = praw.Reddit()
    print 'logged in to Reddit as: ' + str(reddit.user.me())

    subreddit = reddit.subreddit('Showerthoughts')
    for index, submission in enumerate(subreddit.submissions()):
        if index % 100 == 0 and index > 0: print str(index) + ' inserted so far'
        process_submission(connection, cursor, submission)

    cursor.close()
    connection.close()

def process_submission(connection, cursor, submission):
    data_showerthought = (submission.url, submission.title.strip(), int(submission.created_utc))
    try:
        cursor.execute(add_showerthought, data_showerthought)
    except mysql.connector.IntegrityError as err:
        print str(submission.url) + ' has already been inserted. Shutting down.'
        import sys
        sys.exit()
    except:
        print 'Could not insert ' + str(submission.url)
        print submission.title
    finally:
        connection.commit()

if __name__ == '__main__':
    main()