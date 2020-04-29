import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from dashboard.models import Tweet


def city_sentiment():

    df = pd.read_csv("data/sentiment_ratios.csv")
    df = df.set_index("Date")

    data = [go.Scatter(x=df.index, y=df[city], name=city) for city in df.columns]

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
            tick0="2019-01-25"
        ),
        yaxis=dict(title="Sentiment Log Ratio", ticks=""),
        annotations=[
            # dict(
            #     x="2020-02-20",
            #     y=10,
            #     xref="x",
            #     yref="y",
            #     text="1st UK case",
            #     showarrow=True,
            #     arrowhead=7,
            #     ax=0,
            #     ay=-40,
            # ),
            dict(
                x="2020-01-23",
                y=0,
                xref="x",
                yref="y",
                text="First UK Case",
                showarrow=True,
                font=dict(size=12, color="#ffffff"),
                align="center",
                arrowhead=7,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=0,
                # ay=-30,
                ay=-200,
                bordercolor="#c7c7c7",
                borderwidth=1,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8,
            ),
            dict(
                x="2020-02-28",
                y=0,
                xref="x",
                yref="y",
                text="First UK Death",
                showarrow=True,
                font=dict(size=12, color="#ffffff"),
                align="center",
                arrowhead=7,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#636363",
                ax=0,
                # ay=-30,
                ay=-300,
                bordercolor="#c7c7c7",
                borderwidth=1,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=0.8,
            ),
        ],
        height=600,
        width=800,
    )

    output = plot(dict(data=data, layout=layout), output_type="div")

    return output
