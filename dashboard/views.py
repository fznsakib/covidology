from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import plotly.express as px
import copy
import json
import random as rand
import codecs
import time

import dashboard.data as data
import dashboard.graph as graph

from dashboard.models import Tweet
from django.http import JsonResponse

def dashboard(request):

    # Load static graphs -- 0.016s
    plot0_div = codecs.open('dashboard/static/num_tweets.html', 'r').read()
    plot1_div = codecs.open('dashboard/static/most_common_words.html', 'r').read()
    plot2_div = codecs.open('dashboard/static/sentiment_by_keyword.html', 'r').read()
    plot3_div = codecs.open('dashboard/static/cross_correlation.html', 'r').read()
    
    # Load maps -- 1.78s
    plot4_div, latest_date = graph.map()
    plot5_div = codecs.open('dashboard/static/sentiment_map.html', 'r').read()
    
    # Get cases -- 0.658s
    global_cases = data.get_global()
    top10 = data.get_top10()
    top10_countries, top10_cases = zip(*top10)
    
    # Get tweets -- 0.591s
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
