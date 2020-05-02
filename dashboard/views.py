from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import plotly.express as px
import copy
import json

import dashboard.data as data
import dashboard.graph as graph

from dashboard.models import Tweet
from django.http import JsonResponse


def dashboard(request):

    plot4_div, latest_date = graph.map()

    x_data = [0, 1, 2, 3, 4, 5, 6]
    y_data = [x ** 2 for x in x_data]
    # plot0_div = plot(
    #     [Scatter(x=x_data, y=y_data, mode="lines", name="test", opacity=0.8, marker_color="green")],
    #     output_type="div",
    # )
    plot0_div = graph.num_tweets()

    plot1_div = graph.most_common_words()

    plot2_div = plot(
        [Scatter(x=x_data, y=y_data, mode="lines", name="test", opacity=0.8, marker_color="green")],
        output_type="div",
    )
    plot3_div = plot(
        [Scatter(x=x_data, y=y_data, mode="lines", name="test", opacity=0.8, marker_color="green")],
        output_type="div",
    )
    global_cases = data.get_global()
    top10 = data.get_top10()
    top10_countries, top10_cases = zip(*top10)

    return render(
        request,
        "dashboard.html",
        context={
            "plot_div": [plot0_div, plot1_div, plot2_div, plot3_div, plot4_div],
            "country_metrics": [i for i in top10_countries],
            "cases_metrics": [j for j in top10_cases],
            "latest_date": latest_date
        },
    )
