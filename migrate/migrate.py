#!/usr/bin/python
# coding: utf-8

import MySQLdb
import json
from datetime import datetime

db = MySQLdb.connect(
    host='127.0.0.1',
    user='root',
    passwd='',
    db='vanilla'
)
db.set_character_set('utf8')
cur = db.cursor(MySQLdb.cursors.DictCursor)
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

# result lists
users = []
profiles = []
discussions = []
comments = []

draft = []
media = []

cur.execute('SELECT * FROM GDN_User')
for user in cur.fetchall():
    users.append(
        {
            'pk': user['UserID'],
            'model': 'auth.user',
            'fields': {
                'username': user['Name'],
                'password': user['Password'][1:],  # django doesn't use first $
                'email': user['Email'],
                'date_joined': str(user['DateInserted'] or datetime.now()),
                'is_superuser': user['Admin'] == 1,
                'is_staff': user['Admin'] == 1,
            }
        }
    )
    profiles.append(
        {
            'pk': user['UserID'],
            'model': 'core.profile',
            'fields': {
                'user': user['UserID'],
                'image': user['Photo'],
                'last_seen': str(user['DateLastActive'] or datetime.now()),
                'discussion_count': user['CountDiscussions'],
                'comment_count': user['CountComments'],
            }
        }
    )

cur.execute('SELECT * FROM GDN_Discussion')
for discussion in cur.fetchall():

    comment_list = []
    cur.execute('SELECT CommentID FROM GDN_Comment WHERE DiscussionID = %s', discussion['DiscussionID'])
    for comment in cur.fetchall():
        comment_list.append(comment['CommentID'])

    kudos = []
    cur.execute('SELECT UserID FROM GDN_Kudos WHERE DiscussionID = %s', discussion['DiscussionID'])
    for k in cur.fetchall():
        kudos.append(k['UserID'])

    discussions.append(
        {
            'pk': discussion['DiscussionID'],
            'model': 'forum.discussion',
            'fields': {
                'title': discussion['Name'],
                'author': discussion['InsertUserID'],
                'body': discussion['Body'],
                'comments': comment_list,
                'comment_count': discussion['CountComments'],
                'created_time': str(discussion['DateInserted'] or datetime.now()),
                'edited_time': str(discussion['DateUpdated'] or datetime.now()),
                'last_comment': discussion['LastCommentID'] if comment_list else None,
                'last_commenter': discussion['LastCommentUserID'],
                'last_commented': str(discussion['DateLastComment'] or datetime.now()),
                'kudos': kudos,
                'status': 0 if discussion['Closed'] else 1
            }
        }
    )

cur.execute('SELECT * FROM GDN_Comment')
for comment in cur.fetchall():

    kudos = []
    cur.execute('SELECT UserID FROM GDN_Kudos WHERE CommentID = %s', comment['CommentID'])
    for k in cur.fetchall():
        kudos.append(k['UserID'])

    comments.append(
        {
            'pk': comment['CommentID'],
            'model': 'forum.comment',
            'fields': {
                'author': comment['InsertUserID'],
                'body': comment['Body'],
                'created_time': str(comment['DateInserted'] or datetime.now()),
                'edited_time': str(comment['DateUpdated'] or datetime.now()),
                'kudos': kudos,
                'status': 0 if comment['DateDeleted'] else 1
            }
        }
    )

with open('users.json', 'w') as f:
    json.dump(users, f, indent=2)

with open('profiles.json', 'w') as f:
    json.dump(profiles, f, indent=2)

with open('discussions.json', 'w') as f:
    json.dump(discussions, f, indent=2)

with open('comments.json', 'w') as f:
    json.dump(comments, f, indent=2)
