from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter
import pandas as pd
import plotly.express as px

import copy


def dashboard(request):
    x_data = [0, 1, 2, 3, 4, 5, 6]
    y_data = [x ** 2 for x in x_data]
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

    return render(request, "dashboard.html", context={"plot_div": [plot0_div, plot1_div, plot2_div, plot3_div]})

def map(request):
    df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df.drop(df.loc[df['Country/Region']=='Diamond Princess'].index, inplace=True) # Negative value for some reason
    df.drop(df.loc[df['Province/State']=='Diamond Princess'].index, inplace=True)

    latest_date = df.columns[-1]
    df = df.rename(columns={latest_date : 'Confirmed cases'})
    # Add column and concatenate name is province is given
    join_province_and_country = lambda x, y: y if pd.isnull(x) else x + ', ' + y
    df['Location'] = df['Province/State']
    df['Location'] = df['Location'].combine(df['Country/Region'], join_province_and_country)
    fig = px.scatter_mapbox(df, lat="Lat", lon="Long", color='Confirmed cases', size='Confirmed cases',
                  color_continuous_scale=px.colors.sequential.Peach, size_max=50, zoom=2,
                  hover_name="Location", mapbox_style='carto-darkmatter', title='Confirmed COVID-19 Cases as of ' + latest_date)

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
