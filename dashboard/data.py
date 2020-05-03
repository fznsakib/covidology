import csv
import math
import pandas as pd
from datetime import datetime
from collections import Counter
from nltk.corpus import stopwords
import nltk
from dashboard.models import Tweet


urls = {
    "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
}

# Get time range in dates
dates = pd.date_range(start="2019-12-25", end="2020-03-25").tolist()
for i, date in enumerate(dates):
    dates[i] = date.strftime("%Y-%m-%d")
    dates[i] = datetime.strptime(dates[i], "%Y-%m-%d").date()


def get_global():
    cases = []

    df = pd.read_csv(urls["confirmed"])
    cases.append(df.iloc[:, -1].sum())

    df = pd.read_csv(urls["recovered"])
    cases.append(df.iloc[:, -1].sum())

    df = pd.read_csv(urls["deaths"])
    cases.append(df.iloc[:, -1].sum())

    return cases


def get_top10():
    df_confirmed = pd.read_csv(urls["confirmed"])

    # Get top 10 largest by cases
    df_confirmed = df_confirmed.nlargest(10, df_confirmed.columns[-1])

    top10 = []
    top10_dict = {}

    current_date = df_confirmed.iloc[:, -1].name

    # Get country name and number of cases for each country
    for index, row in df_confirmed.iterrows():
        country = ""

        # If there is state named, add to country name
        if not str(row["Province/State"]) == "nan":
            country = str(row["Province/State"]) + ", "

        country += row["Country/Region"]
        cases = row[current_date]

        top10.append([country, cases])

    return top10


def get_map_data():
    df = pd.read_csv(urls["confirmed"])
    df_deaths = pd.read_csv(urls["deaths"])
    df.drop(
        df.loc[df["Country/Region"] == "Diamond Princess"].index, inplace=True
    )  # Negative value for some reason
    df.drop(df.loc[df["Province/State"] == "Diamond Princess"].index, inplace=True)
    df.drop(df.loc[df["Province/State"] == "Grand Princess"].index, inplace=True)

    latest_date = df.columns[-1]
    df = df.rename(columns={latest_date: "Confirmed cases"})
    # Add column and concatenate name is province is given
    join_province_and_country = lambda x, y: y if pd.isnull(x) else x + ", " + y
    df["Location"] = df["Province/State"]
    df["Location"] = df["Location"].combine(df["Country/Region"], join_province_and_country)
    df["Deaths"] = df_deaths[df_deaths.columns[-1]]

    return df, latest_date


def get_num_tweets():
    num_tweets = {"negative": [], "positive": [], "neutral": []}

    for date in dates:
        tweets_on_date = Tweet.objects.filter(date=date)

        negative_tweets = tweets_on_date.filter(output="N")
        positive_tweets = tweets_on_date.filter(output="P")
        neutral_tweets = tweets_on_date.filter(output="Neutral")

        num_tweets["negative"].append(len(negative_tweets))
        num_tweets["positive"].append(len(positive_tweets))
        num_tweets["neutral"].append(len(neutral_tweets))

    return num_tweets, dates


def compute_most_common_words():

    words = []

    tweets = Tweet.objects.all()

    # Define stop words
    s = stopwords.words("english")
    extra_stopwords = [
        "…",
        "I",
        ".",
        ",",
        "!",
        "?",
        ":",
        "-",
        "&",
        "...",
        "'",
        '"',
        "``",
        "''",
        "The",
        "like",
        "This",
        "A",
        "it's",
        "%",
    ]
    s.extend(extra_stopwords)
    s = set(s)

    # Filter tweets
    for tweet in tweets:
        text = filter(lambda w: not w in s, tweet.cleaned_tweet.split())

        for word in text:
            words.append(word)

    # Get top n words used in tweets
    word_counter = Counter(words)
    most_occur = word_counter.most_common(2000)

    # Remove case sensitive duplicates of words
    cleaned_most_occur = {}

    for i, entry in enumerate(most_occur):

        word_found = False

        for j, key in enumerate(cleaned_most_occur.keys()):
            if entry[0].lower() == key.lower():
                cleaned_most_occur[key] += entry[1]
                word_found = True
                break

        if not word_found:
            cleaned_most_occur[entry[0]] = entry[1]

    print(cleaned_most_occur)
    print(len(cleaned_most_occur))

    # Export to CSV for quicker access
    with open("data/top_words.csv", "w") as csvfile:
        fieldnames = ["Word", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i, word in enumerate(cleaned_most_occur.keys()):
            writer.writerow({"Word": word, "Count": cleaned_most_occur[word]})

    return cleaned_most_occur


# Calculate proportion of negative tweets per day for every city
def compute_sentiment_proportions():

    sentiment_dict = {
        "London": [],
        "Bristol": [],
        "Manchester": [],
        "Liverpool": [],
        "Birmingham": [],
        "Leeds": [],
        "Oxford": [],
        "Glasgow": [],
        "Dublin": [],
        "Cardiff": [],
        "Total": [],
    }

    for date in dates:
        # filter tweets by date
        tweets_on_date = Tweet.objects.filter(date=date)

        for city in sentiment_dict.keys():

            # filter tweets by city if total sentiment is not being collected
            if city != "Total":
                filtered_dates = tweets_on_date.filter(city=city)
            else:
                filtered_dates = tweets_on_date

            # get positive/negative tweets for date/city
            positive_tweets = filtered_dates.filter(output="P")
            neutral_tweets = filtered_dates.filter(output="Neutral")
            negative_tweets = filtered_dates.filter(output="N")
            total_num_tweets = len(positive_tweets) + len(neutral_tweets) + len(negative_tweets)

            # value for when no tweets exist for this date/city
            if total_num_tweets == 0:
                # A value of 0 is used to show there are no tweets
                sentiment_dict[city].append(0)
                continue

            sentiment_proportion = len(neutral_tweets) / total_num_tweets

            sentiment_dict[city].append(sentiment_proportion)

    sentiment_dict["Date"] = dates

    # Export to CSV for quicker access
    with open("neutral_proportions.csv", "w") as csvfile:
        fieldnames = sentiment_dict.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i, date in enumerate(sentiment_dict["Date"]):
            writer.writerow(
                {
                    "Date": date,
                    "London": sentiment_dict["London"][i],
                    "Bristol": sentiment_dict["Bristol"][i],
                    "Manchester": sentiment_dict["Manchester"][i],
                    "Liverpool": sentiment_dict["Liverpool"][i],
                    "Birmingham": sentiment_dict["Birmingham"][i],
                    "Leeds": sentiment_dict["Leeds"][i],
                    "Oxford": sentiment_dict["Oxford"][i],
                    "Glasgow": sentiment_dict["Glasgow"][i],
                    "Dublin": sentiment_dict["Dublin"][i],
                    "Cardiff": sentiment_dict["Cardiff"][i],
                    "Total": sentiment_dict["Total"][i],
                }
            )


def compute_sentiment_proportions_by_word():
    words = [
        "coronavirus",
        "COVID-19",
        "government",
        "NHS",
        "BBC",
        "Boris",
        "London",
        "cancelled",
        "lockdown",
        "Trump",
    ]

    sentiment_dict = {}

    for word in words:
        sentiment_dict[word] = []

        tweets = Tweet.objects.filter(cleaned_tweet__icontains=word)

        positive_tweets = tweets.filter(output="P")
        neutral_tweets = tweets.filter(output="Neutral")
        negative_tweets = tweets.filter(output="N")
        total_num_tweets = len(positive_tweets) + len(neutral_tweets) + len(negative_tweets)

        positive_proportion = (len(positive_tweets) / total_num_tweets) * 100
        neutral_proportion = (len(neutral_tweets) / total_num_tweets) * 100
        negative_proportion = (len(negative_tweets) / total_num_tweets) * 100

        sentiment_dict[word].append(positive_proportion)
        sentiment_dict[word].append(neutral_proportion)
        sentiment_dict[word].append(negative_proportion)
        sentiment_dict[word].append(total_num_tweets)

    # Export to CSV for quicker access
    with open("data/sentiment_by_keyword.csv", "w") as csvfile:
        fieldnames = ["Word", "Positive", "Neutral", "Negative", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i, word in enumerate(sentiment_dict.keys()):
            writer.writerow(
                {
                    "Word": word,
                    "Positive": sentiment_dict[word][0],
                    "Neutral": sentiment_dict[word][1],
                    "Negative": sentiment_dict[word][2],
                    "Count": sentiment_dict[word][3],
                }
            )
