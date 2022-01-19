from hashlib import md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s
import html
import re, sys, configparser
from datetime import datetime
import pandas as pd
pd.options.mode.chained_assignment = None 
import numpy as np

if __name__ == '__main__':
    
    src = str(sys.argv[1])
    dest = str(sys.argv[2])
    print('Reading data from ',src)
    df = pd.read_csv(src)
    
    df1 = df[['date', 'title']]
    df1['title'] = df1['title'].astype(str).apply(lambda x: html.unescape(x))
    df1['text'] = df['fullText'].astype(str).apply(lambda x: html.unescape(x))
    df1['url'] = df['url']
    df1['text_language'] = df['language']
    df1['sentiment'] = df['sentiment']
    df1['emotion'] = df['classifications']
    df1['impact'] = df['impact']
    df1['reach_estimate'] = df['reachEstimate']
    df1['professions'] = df['professions']
    df1['media_urls'] = df['mediaUrls']
    df1['subtype'] = df['publisherSubType']
    df1['engagement_type'] = df['engagementType']
    df1['Page_post_id'] = df['guid']
    df1['user_id'] = df['facebookAuthorId']
    df1['user_name'] = df['fullname']
    df1['user_gender'] = df['gender']
    df1['facebook_comments'] = df['facebookComments']
    df1['facebook_likes'] = df['facebookLikes']
    df1['facebook_role'] = df['facebookRole']
    df1['facebook_shares'] = df['facebookShares']
    df1['facebook_subtype'] = df['facebookSubtype']
    df1['facebook_updated'] = df['updated']
    df1['matchPositions'] = df['matchPositions']
    df1['thread_id'] = df['threadId']
    df1['thread_author'] = df['threadAuthor'].astype(str).apply(lambda x: html.unescape(x))
    df1['thread_created'] = df['threadCreated']
    df1['thread_entry_type'] = df['threadEntryType']
    df1['thread_url'] = df['threadURL']

    df1.to_csv(dest,escapechar="\\", index=False)
    print('Datasets are merged and saved to ', dest)
