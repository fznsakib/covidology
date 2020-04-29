import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from dashboard.models import Tweet


def city_sentiment():

    df = pd.read_csv("data/sentiment_ratios.csv")
    df = df.set_index("Date")

    print(df)
    print(df.index)

    # Create graph
    # x_data = df["Date"]
    # y_data = df["London"]
    # y=immigration.loc[state],  name=state) for state in immigration.index
    # trace_london = Scatter(
    #     x=x_data,
    #     y=y_data,
    #     mode="lines",
    #     name="sentiment_by_city",
    #     opacity=0.8,
    #     marker_color="green",
    # )

    print(df.columns)
    # data = [
    #     go.Scatter(x=df.index, y=df.loc[city], name=city)
    #     for city in df.columns
    # ]
    data = [go.Scatter(x=df.index, y=df[city], name=city) for city in df.columns]

    #  y=immigration.loc[state],
    #                name=state) for state in immigration.index]

    # data = [trace_london]

    layout = go.Layout(
        # title='Win Probability Matrix',
        xaxis=dict(title="Date", ticks="", rangeslider_visible=True),
        yaxis=dict(title="Sentiment Log Ratio", ticks=""),
        height=600,
        width=800,
    )

    output = plot(dict(data=data, layout=layout), output_type="div")

    return output
