#!/usr/bin/python
#coding: utf-8

import MySQLdb
import json

db = MySQLdb.connect(
    host='127.0.0.1',
    user='',
    passwd='',
    db='vanilla'
)
cur = db.cursor(MySQLdb.cursors.DictCursor)

# result lists
users = []
profiles = []
discussions = []
comments = []
kudos = []

cur.execute('SELECT * FROM GDN_User')
for user in cur.fetchall():
    users.append(
        {
            'pk': user['UserID'],
            'model': 'auth.user',
            'fields': {
                'username': user['Name'],
                'password': user['Password'],
                'email': user['Email'],
            }
        }
    )
    profiles.append(
        {
            'pk': user['UserID'],
            'model': 'core.profile',
            'fields': {
                'image': user['Photo'],
            }
        }
    )

cur.execute('SELECT * FROM GDN_Discussion')
for discussion in cur.fetchall():

    comment_list = []
    cur.execute('SELECT CommentID FROM GDN_Comment WHERE DiscussionID = %s', discussion['DiscussionID'])
    for comment in cur.fetchall():
        comment_list.append(comment['CommentID'])

    discussions.append(
        {
            'pk': discussion['DiscussionID'],
            'model': 'forum.discussion',
            'fields': {
                'title': discussion['Name'],
                'author': discussion['InsertUserID'],
                'body': discussion['Body'],
                'comments': comment_list,
                #'': discussion['CountComments'],
                #'': discussion['DateInserted'],
                #'': discussion['DateUpdated'],
                #'last_comment_id': discussion['LastCommentID'],
                #'last_comment_user_id': discussion['LastCommentUserID'],
            }
        }
    )

cur.execute('SELECT * FROM GDN_Comment')
for comment in cur.fetchall():
    comments.append(
        {
            'pk': comment['CommentID'],
            'model': 'forum.comment',
            'fields': {
                'title': comment['Name'],
                'author': comment['InsertUserID'],
                'body': comment['Body'],
                #'': comment['DateInserted'],
                #'': comment['DateUpdated'],
                #'': comment['DateDeleted'],
                #'last_comment_id': comment['LastCommentID'],
                #'last_comment_user_id': comment['LastCommentUserID'],
            }
        }
    )

kudos_id = 0
cur.execute('SELECT * FROM GDN_Kudos')
for kudo in cur.fetchall():
    kudos_id += 1
    kudos.append(
        {
            'pk': kudos_id,
            'model': 'forum.kudos',
            'fields': {
                'kudos': kudo['UserID'],
                'given': kudo['DateUpdated'],
                #'': kudo['CommentID'],
                #'': kudo['DiscussionID'],
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

with open('kudos.json', 'w') as f:
    json.dump(kudos, f, indent=2)
