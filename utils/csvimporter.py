import sys, os
import django
import csv
import pandas as pd

############ All you need to modify is below ############
# Full path and name to your csv file
csv_filepathname = "/Users/faizaan/Documents/University/2019-2020/Applied Data Science/COVID-19-sentiment-analysis/data/news.csv"
# Full path to the directory immediately above your django project directory
your_djangoproject_home = (
    "/Users/faizaan/Documents/University/2019-2020/Applied Data Science/COVID-19-sentiment-analysis"
)
############ All you need to modify is above ############

sys.path.append(your_djangoproject_home)
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"

django.setup()
from dashboard.models import Article

dataReader = csv.reader(open(csv_filepathname), delimiter=",", quotechar='"')

for i, row in enumerate(dataReader):
    if i == 0:
        continue

    article = Article()
    article.article_id = row[0]
    article.date = row[2]
    article.section = row[1]
    article.headline = row[3]
    article.url = row[4]
    article.article = row[5]
    article.save()
    # ftse=FTSE()
    # ftse.date = row[0]
    # ftse.open = row[1]
    # ftse.close = row[2]
    # ftse.high = row[3]
    # ftse.low = row[4]
    # ftse.volume = row[5]
    # ftse.save()
    # tweet.tweet_id=row[0]
    # tweet.date=row[1]
    # tweet.time=row[2]
    # tweet.username=row[4]
    # tweet.tweet=row[7]
    # tweet.replies_count=row[11]
    # tweet.retweets_count=row[12]
    # tweet.likes_count=row[13]
    # tweet.city=row[19]
    # tweet.popular=row[21]
    # tweet.verified=row[22]
    # tweet.output=row[24]
    # tweet.positive=row[25]
    # tweet.negative=row[26]

    # tweet.save()

# p = Tweet(tweet_id=row['id'], date=row['date'], time=row['time'], username=row['username'], tweet=row['tweet'], city=row['near'], replied_count=row['replies_count'], retweets_count['retweets_count'], likes_count=row['likes_count'], popular=row['popular'], verified=row['verified'], output=row['w2v_out'], positive=row['w2v_P_conf'], negative=row['w2v_N_conf'])

# tweet.tweet_id=row['id']
# tweet.date=row['date']
# tweet.time=row['time']
# tweet.username=row['username']
# tweet.tweet=row['tweet']
# tweet.city=row['near']
# tweet.replies_count=row['replies_count']
# tweet.retweets_count['retweets_count']
# tweet.likes_count=row['likes_count']
# tweet.popular=row['popular']
# tweet.verified=row['verified']
# tweet.output=row['output']
# tweet.positive=row['positive']
# tweet.negative=row['negative']
