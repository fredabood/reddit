import praw
import os
import ast
from pprint import pprint
import json

creds = ast.literal_eval(os.environ['REDDIT_CREDS'])

reddit = praw.Reddit(client_id=creds['client_id'],
                     client_secret=creds['client_secret'],
                     user_agent=creds['user_agent'],
                     username=creds['username'],
                     password=creds['password'])

with open('data.json') as datafile:
    celebs = json.load(datafile)

for celeb in celebs:
    
    profile = reddit.redditor(celebs[celeb]['username'])
    top_comments = profile.comments.top(limit=None)
    comment_bodies = []

    for comment in top_comments:
        comment_bodies.append(comment.body)

    celebs[celeb]['comments'] = comment_bodies

with open('data.json', 'w') as datafile:
    json.dump(celebs, datafile)
