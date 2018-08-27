import praw
import os
import ast
from pprint import pprint
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd


def comment_data_gen(comment):    
    '''
    This function takes in PRAW's comment object, and outputs a dictionary containing key data about the comment.
    
    text: the text body of the comment
    length: the character count of the comement
    utc_timestamp: the timestamp of comment creation
    subreddit: the sub where the comment was made
    score: upvotes, downvotes, and combined score
    vader: the compound, positive, negative, and neutral vader scores
    
    Sample Dict:
    
    {
        "text": "Here's the body text of the comment.",
        "vader": {
          "neg": 0.189,
          "neu": 0.811,
          "pos": 0,
          "compound": -0.5423
        },
        "length": 143,
        "timestampUTC": 1474305662,
        "score": {
          "compound": 1074,
          "ups": 1074,
          "downs": 0
        },
        "subreddit": "r/politics"
    }
    
    '''
    
    analyzer = SentimentIntensityAnalyzer()
    results = analyzer.polarity_scores(comment.body)
    
    return dict(
        text = comment.body,
        length = len(comment.body),
        utc_timestamp = comment.created_utc,
        subreddit = comment.subreddit_name_prefixed,
        score = dict(
            compound = comment.score,
            ups = comment.ups,
            downs = comment.downs
        ),
        vader = results
    )


def celeb_data_gen(username, reddit):

    '''
    This function takes in a reddit username, and outputs a dictionary containing key data about the comments made by that user.
    
    username: the user's reddit username
    commentCount: number of comments made by the user
    avgCommentLenth: average length of the user's comments
    vader: dictionary containing the average compound, negative, neutral, and positive vader scores
    avgScore: dictionary containing the users average compound score, upvotes, and dounvotes
    comments: a list of dictionaries ouput by comment_data_gen()
    
    Sample Data:
    
    {
        "username": "aclu",
        "commentCount": 41,
        "avgCommentLenth": 230.3658536585366,
        "vader": {
            "compound": 0.34544878048780486,
            "neg": 0.03953658536585366,
            "neu": 0.7870487804878048,
            "pos": 0.17346341463414633
        },
        "avgScore": {
            "compound": 2451.5365853658536,
            "ups": 2451.5365853658536,
            "douns": 0
        },
        "comments": [
            {
                "text": "Here's the body text of the comment.",
                "vader": {
                    "neg": 0.189,
                    "neu": 0.811,
                    "pos": 0,
                    "compound": -0.5423
                },
                "length": 143,
                "timestampUTC": 1474305662,
                "score": {
                    "compound": 1074,
                    "ups": 1074,
                    "downs": 0
                },
                "subreddit": "r/politics"
            }
        ]
    }
    '''
    
    profile = reddit.redditor(username)
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

        comment_data = comment_data_gen(comment)
        
        comments.append(comment_data)

        compound_list.append(comment_data['vader']['compound'])
        positive_list.append(comment_data['vader']["pos"])
        negative_list.append(comment_data['vader']["neg"])
        neutral_list.append(comment_data['vader']["neu"])

        score_list.append(comment_data['score']['compound'])
        ups_list.append(comment_data['score']['ups'])
        downs_list.append(comment_data['score']['downs'])

        comment_lengths.append(len(comment_data['text']))
        
    
    return dict(
        username = username,
        commentCount = len(comments),
        avgCommentLenth = np.mean(comment_lengths),
        vader = dict(
            compound = np.mean(compound_list),
            neg = np.mean(negative_list),
            neu = np.mean(neutral_list),
            pos = np.mean(positive_list)
        ),
        avgScore = dict(
            compound = np.mean(score_list),
            ups = np.mean(ups_list),
            douns = np.mean(downs_list)
        ),
        comments = comments
    )


def update_json(filepath, return_df=False):
    
    '''
    Updates the JSON datafile, and reads to DF for analysis.
    '''
    
    creds = ast.literal_eval(os.environ['REDDIT_CREDS'])

    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'],
                         username=creds['username'],
                         password=creds['password'])
    
    # Read data from JSON
    with open(filepath,'r') as datafile:
        celebs = json.load(datafile)
    
    # Updating the JSON file
    for celeb in celebs:
        celebs[celeb] = celeb_data_gen(celebs[celeb]['username'], reddit)
    
    # Write output to JSON
    with open(filepath, 'w') as datafile:
        json.dump(celebs, datafile)
    
    if return_df==True:
        return pd.read_json(filepath)


if __name__ == "__main__":
    
    update_json('data.json')

