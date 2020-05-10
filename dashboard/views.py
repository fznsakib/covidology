from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import plotly.express as px
import copy
import json
import random as rand

import dashboard.data as data
import dashboard.graph as graph

from dashboard.models import Tweet
from django.http import JsonResponse


def dashboard(request):

    plot5_div = graph.city_sentiment_map()
    plot4_div, latest_date = graph.map()

    plot0_div = graph.num_tweets()

    plot1_div = graph.most_common_words()

    plot2_div = graph.sentiment_by_words()

    plot3_div = graph.cross_correlation()

    global_cases = data.get_global()
    top10 = data.get_top10()
    top10_countries, top10_cases = zip(*top10)

    random_tweets = data.get_random_example_tweet()
    random_positive_tweet = random_tweets["positive"][0]
    random_neutral_tweet = random_tweets["neutral"][0]
    random_negative_tweet = random_tweets["negative"][0]

    return render(
        request,
        "dashboard.html",
        context={
            "plot_div": [plot0_div, plot1_div, plot2_div, plot3_div, plot4_div, plot5_div],
            "country_metrics": [i for i in top10_countries],
            "cases_metrics": [j for j in top10_cases],
            "random_tweets": [random_positive_tweet, random_neutral_tweet, random_negative_tweet],
            "latest_date": latest_date,
        },
    )
