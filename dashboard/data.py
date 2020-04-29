import csv
import math
import pandas as pd
from datetime import datetime
from dashboard.models import Tweet

urls = {
    "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
}


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


def compute_sentiment_ratio():

    # Get time range in dates
    dates = pd.date_range(start="2019-12-25", end="2020-03-25").tolist()
    for i, date in enumerate(dates):
        dates[i] = date.strftime("%Y-%m-%d")
        dates[i] = datetime.strptime(dates[i], "%Y-%m-%d").date()

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

            # value for when no tweets exist for this date/city
            if len(filtered_dates) == 0:
                # A value of -1 is used to show there are no tweets
                sentiment_dict[city].append(-1)
                continue

            # get positive/negative tweets for date/city
            positive_tweets = filtered_dates.filter(output="P")
            negative_tweets = filtered_dates.filter(output="N")

            # compute log ratio of num positive tweets/num negative tweets
            if len(negative_tweets) == 0:
                sentiment_dict[city].append(0)
                continue
            elif len(positive_tweets) == 0:
                ratio = len(negative_tweets)
            else:
                ratio = len(negative_tweets) / len(positive_tweets)

            log_ratio = math.log(ratio)

            sentiment_dict[city].append(log_ratio)

    sentiment_dict["Date"] = dates

    # Export to CSV for quicker access
    with open("sentiment_ratios.csv", "w") as csvfile:
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
