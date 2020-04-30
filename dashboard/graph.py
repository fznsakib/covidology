import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dashboard.data as data
from plotly.offline import plot
from plotly.graph_objs import Scatter
from dashboard.models import Tweet


def city_sentiment():

    df = pd.read_csv("data/negative_proportions.csv")
    df = df.set_index("Date")

    traces = [go.Scatter(x=df.index, y=df[city], name=city) for city in df.columns]

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
                x=0.82,
                activecolor="powderblue",
                bordercolor="powderblue",
                borderwidth=1
                # yanchor="middle"
            ),
            type="date",
            tick0="2019-01-25",
        ),
        yaxis=dict(title="Sentiment Log Ratio", ticks=""),
        # annotations=[
        #     dict(
        #         x="2020-01-23",
        #         y=2.5,
        #         xref="x",
        #         yref="y",
        #         text="1st UK Case",
        #         showarrow=True,
        #         font=dict(size=12, color="#ffffff"),
        #         align="center",
        #         arrowhead=6,
        #         arrowsize=1,
        #         arrowwidth=1,
        #         arrowcolor="#636363",
        #         ax=0,
        #         # ay=-30,
        #         ay=-100,
        #         bordercolor="#c7c7c7",
        #         borderwidth=2,
        #         borderpad=4,
        #         bgcolor="steelblue",
        #         opacity=0.8,
        #     ),
        #     dict(
        #         x="2020-02-28",
        #         y=5.5,
        #         xref="x",
        #         yref="y",
        #         text="1st UK Death",
        #         showarrow=True,
        #         font=dict(size=12, color="#ffffff"),
        #         align="center",
        #         arrowhead=6,
        #         arrowsize=1,
        #         arrowwidth=1,
        #         arrowcolor="#636363",
        #         ax=0,
        #         # ay=-30,
        #         ay=-40,
        #         bordercolor="#c7c7c7",
        #         borderwidth=1,
        #         borderpad=4,
        #         bgcolor="#ff7f0e",
        #         opacity=0.8,
        #     ),
        # ],
        # height=400,
        # width=600,
    )
    # config={'responsive': True}
    output = plot(dict(data=traces, layout=layout), output_type="div")

    return output


def map():
    df = data.get_map_data()
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
        # title="Confirmed COVID-19 Cases as of "
        # + latest_date
        # + " (source:https://github.com/CSSEGISandData/COVID-19)",
    )

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
    output = plot(fig, output_type="div")
    return output


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
                x=0.7,
                activecolor="powderblue",
                bordercolor="powderblue",
                borderwidth=1
                # yanchor="middle"
            ),
            type="date",
            tick0="2019-01-25",
        ),
        yaxis=dict(title="Number of Tweets", ticks=""),
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
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.25,
                yanchor="top",
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
                # ay=-30,
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
                # ay=-30,
                ay=-120,
                bordercolor="#c7c7c7",
                borderwidth=1,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8,
            ),
        ]
        # height=400,
        # width=600,
    )

    output = plot(dict(data=traces, layout=layout), output_type="div")

    return output


def most_common_words():
    words = data.get_most_common_words()

    # print(words)
