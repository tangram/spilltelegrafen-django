#!/usr/bin/python
# coding: utf-8

import MySQLdb
import json

db = MySQLdb.connect(
    host='127.0.0.1',
    user='root',
    passwd='',
    db='vanilla'
)
cur = db.cursor(MySQLdb.cursors.DictCursor)

# result lists
users = []
profiles = []
discussions = []
comments = []

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
                'date_joined': user['DateInserted'],
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
                'image': user['Photo'],
                #'last_seen': user['DateLastActive'],
                #'discussion_count': user['CountDiscussions'],
                #'comment_count': user['CountComments'],
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

    if not discussion['DateDeleted']:
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
                    #'': discussion['DateInserted'],
                    #'': discussion['DateUpdated'],
                    #'last_comment_id': discussion['LastCommentID'],
                    'last_commenter': discussion['LastCommentUserID'],
                    'kudos': kudos,
                }
            }
        )

cur.execute('SELECT * FROM GDN_Comment')
for comment in cur.fetchall():

    kudos = []
    cur.execute('SELECT UserID FROM GDN_Kudos WHERE CommentID = %s', discussion['CommentID'])
    for k in cur.fetchall():
        kudos.append(k['UserID'])

    if not comment['DateDeleted']:
        comments.append(
            {
                'pk': comment['CommentID'],
                'model': 'forum.comment',
                'fields': {
                    'author': comment['InsertUserID'],
                    'body': comment['Body'],
                    #'': comment['DateInserted'],
                    #'': comment['DateUpdated'],
                    #'': comment['DateDeleted'],
                    'kudos': kudos,
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
