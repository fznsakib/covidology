import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dashboard.data as data
import datetime
from plotly.offline import plot
from plotly.graph_objs import Scatter
from dashboard.models import Tweet

config = {"displaylogo": False, "scrollZoom": True, 'responsive': True}


def map():
    df, latest_date = data.get_map_data()
    list_of_hover_data = ["Confirmed cases", "Deaths"]
    fig = px.scatter_mapbox(
        df,
        lat="Lat",
        lon="Long",
        color="Confirmed cases",
        size="Confirmed cases",
        color_continuous_scale=px.colors.sequential.Peach,
        size_max=50,
        zoom=2,
        hover_name="Location",
        hover_data=list_of_hover_data,
        mapbox_style="carto-darkmatter",
    )

    fig.update_layout(
        autosize=True,
        width=1500,
        height=600,
        margin=dict(l=10, r=700, b=10, t=10, pad=4),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Raleway", color="#FFFFFF"),
    )
    output = plot(fig, output_type="div")
    
    # Convert date format and return to display on page
    latest_date = datetime.datetime.strptime(latest_date, '%m/%d/%y').strftime('%d/%m/%y')
    
    return output, latest_date


def num_tweets():
    # get positive, negative, neutral tweet numbers per day
    num_tweets, dates = data.get_num_tweets()

    colours = ["#00CC96", "#EF553B", "#636EFA"]

    traces = [
        go.Scatter(x=dates, y=num_tweets[sentiment_type], name=sentiment_type)
        for i, sentiment_type in enumerate(num_tweets.keys())
    ]

    layout = go.Layout(
        # title='Win Probability Matrix',
        xaxis=dict(
            title="Date",
            ticks="",
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=7, label="1w", step="day", stepmode="backward"),
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=3, label="3m", step="month", stepmode="backward")
                        # dict(step="all"),
                    ]
                ),
                x=0.75,
                y=1.08,
                activecolor="powderblue",
                bordercolor="powderblue",
                font=dict(
                    color="#000000"
                ),
                borderwidth=1,
            ),
            type="date",
            tick0="2019-01-25",
            gridcolor="#FFFFFF",
        ),
        yaxis=dict(title="Number of Tweets", ticks="", gridcolor="#FFFFFF"),
        updatemenus=[
            dict(
                buttons=list(
                    [
                        dict(
                            label="All",
                            method="update",
                            args=[{"visible": [True, True, True]}, {"showlegend": True}],
                        ),
                        dict(
                            label="Negative",
                            method="update",
                            args=[{"visible": [True, False, False]},],
                        ),
                        dict(
                            label="Positive",
                            method="update",
                            args=[{"visible": [False, True, False]},],
                        ),
                        dict(
                            label="Neutral",
                            method="update",
                            args=[{"visible": [False, False, True]},],
                        ),
                    ]
                ),
                direction="down",
                # pad={"r": 10, "t": 10},
                showactive=False,
                x=0.23,
                y=1.15,
            ),
        ],
        annotations=[
            dict(
                x="2020-01-23",
                y=0,
                xref="x",
                yref="y",
                text="1st UK Case",
                showarrow=True,
                font=dict(size=10, color="#ffffff"),
                align="center",
                arrowhead=6,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor="#636363",
                ax=0,
                ay=-100,
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                bgcolor="steelblue",
                opacity=0.8,
            ),
            dict(
                x="2020-02-28",
                y=0,
                xref="x",
                yref="y",
                text="1st UK Death",
                showarrow=True,
                font=dict(size=10, color="#ffffff"),
                align="center",
                arrowhead=6,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor="#636363",
                ax=0,
                ay=-120,
                bordercolor="#c7c7c7",
                borderwidth=1,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8,
            ),
        ],
        paper_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        plot_bgcolor="rgba(255,255,255,0.9)",
        font=dict(family="Raleway", color="#FFFFFF"),
        margin=dict(l=1, r=1, b=1, t=1, pad=0),
    )

    output = plot(dict(data=traces, layout=layout), config=config, output_type="div")

    return output


def most_common_words():

    df = pd.read_csv("data/top_words.csv")

    df = df[df.Word != "coronavirus"]
    df = df[df.Word != "COVID-19"]

    df = df.sort_values("Count")
    df = df.tail(20)

    traces = [go.Bar(x=df["Count"], y=df["Word"], orientation="h")]

    layout = go.Layout(
        xaxis=dict(title="Frequency", gridcolor="#FFFFFF"),
        yaxis=dict(title="Word", ticks="", gridcolor="#FFFFFF"),
        paper_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        font=dict(
            family="Raleway",
            color="#FFFFFF",
        ),
        plot_bgcolor="rgba(255,255,255,0.9)",
        margin=dict(l=1, r=1, b=1, t=1, pad=0),
    )

    output = plot(dict(data=traces, layout=layout), config=config, output_type="div")

    return output
