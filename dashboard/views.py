from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import plotly.express as px
import copy

import dashboard.data as data

from dashboard.models import Tweet

def dashboard(request):   

    x_data = [0, 1, 2, 3, 4, 5, 6]
    y_data = [x ** 2 for x in x_data]
    m_data = [i for i in range(10)]
    plot0_div = plot(
        [Scatter(x=x_data, y=y_data, mode="lines", name="test", opacity=0.8, marker_color="green")],
        output_type="div",
    )
    plot1_div = plot(
        [Scatter(x=x_data, y=y_data, mode="lines", name="test", opacity=0.8, marker_color="green")],
        output_type="div",
    )
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

    plot4_div = plot(
        [Scatter(x=m_data, y=top10[0:], mode="lines", name="test", opacity=0.8, marker_color="green")],
        output_type="div",
    )

    return render(request, "dashboard.html", context={"plot_div": [plot0_div, plot1_div, plot2_div, plot3_div,plot4_div]})

def map(request):
    df = pd.read_csv(data.urls['confirmed'])
    df_deaths = pd.read_csv(data.urls['deaths'])
    df.drop(df.loc[df['Country/Region']=='Diamond Princess'].index, inplace=True) # Negative value for some reason
    df.drop(df.loc[df['Province/State']=='Diamond Princess'].index, inplace=True)
    df.drop(df.loc[df['Province/State']=='Grand Princess'].index, inplace=True)

    latest_date = df.columns[-1]
    df = df.rename(columns={latest_date : 'Confirmed cases'})
    # Add column and concatenate name is province is given
    join_province_and_country = lambda x, y: y if pd.isnull(x) else x + ', ' + y
    df['Location'] = df['Province/State']
    df['Location'] = df['Location'].combine(df['Country/Region'], join_province_and_country)
    df['Deaths'] = df_deaths[df_deaths.columns[-1]]
    list_of_hover_data = ["Confirmed cases","Deaths"]
    fig = px.scatter_mapbox(df, lat="Lat", lon="Long", color='Confirmed cases', size='Confirmed cases',
                  color_continuous_scale=px.colors.sequential.Peach, size_max=50, zoom=2,
                  hover_name="Location", hover_data=list_of_hover_data, mapbox_style='carto-darkmatter', title='Confirmed COVID-19 Cases as of '
                  + latest_date
                  + " (source:https://github.com/CSSEGISandData/COVID-19)")

    fig.update_layout(
        autosize=True,
        # width=500,
        height=800,
        # margin=dict(
        #     l=50,
        #     r=50,
        #     b=100,
        #     t=100,
        #     pad=4
        # ),
        # paper_bgcolor="#75DEAA",
    )
    figure = plot(fig, output_type="div")


    return render(request, "map.html", context={"map_div": figure})
