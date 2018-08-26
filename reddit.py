import praw
import os
import ast
from pprint import pprint
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np

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

    comments = []

    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []

    score_list = []
    ups_list = []
    downs_list = []

    comment_lengths = []

    for comment in top_comments:

        comment_data = {}

        comment_data['text'] = comment.body

        analyzer = SentimentIntensityAnalyzer()
        results = analyzer.polarity_scores(comment.body)
        comment_data['vader'] = results

        compound_list.append(results['compound'])
        positive_list.append(results["pos"])
        negative_list.append(results["neg"])
        neutral_list.append(results["neu"])

        comment_data['length'] = len(comment_data['text'])
        comment_lengths.append(len(comment_data['text']))
        comment_data['timestampUTC'] = comment.created_utc

        comment_data['score'] = {
            'compound': comment.score,
            'ups': comment.ups,
            'downs': comment.downs
        }

        score_list.append(comment.score)
        ups_list.append(comment.ups)
        downs_list.append(comment.downs)

        comment_data['subreddit'] = comment.subreddit_name_prefixed

        comments.append(comment_data)


    celebs[celeb]['comments'] = comments

    celebs[celeb]['vader'] = {
        'compound': np.mean(compound_list),
        'neg': np.mean(negative_list),
        'neu': np.mean(neutral_list),
        'pos': np.mean(positive_list)
    }

    celebs[celeb]['commentCount'] = len(celebs[celeb]['comments'])
    celebs[celeb]['avgCommentLenth'] = np.mean(comment_lengths)
    celebs[celeb]['avgScore'] = {
        'compound':np.mean(score_list),
        'ups': np.mean(ups_list),
        'douns': np.mean(downs_list)
    }

    print(celeb)


with open('data.json', 'w') as datafile:
    json.dump(celebs, datafile)
