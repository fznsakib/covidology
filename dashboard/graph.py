import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dashboard.data as data
import datetime
from plotly.offline import plot
from plotly.graph_objs import Scatter
from dashboard.models import Tweet

config = {"displaylogo": False, "scrollZoom": True, "responsive": True}


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
    latest_date = datetime.datetime.strptime(latest_date, "%m/%d/%y").strftime("%d/%m/%y")

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
                # x=0.75,
                # y=1.08,
                activecolor="powderblue",
                bordercolor="powderblue",
                font=dict(color="#000000"),
                borderwidth=1,
                yanchor="bottom",
            ),
            type="date",
            tick0="2019-01-25",
            gridcolor="#FFFFFF",
            showgrid=True,
            showline=True,
            linecolor="rgb(102, 102, 102)",
            tickfont_color="rgb(255, 255, 255)",
            showticklabels=True,
            ticks="outside",
            tickcolor="rgb(255, 255, 255)",
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
                x=1,
                # y=1.15,
                xanchor="right",
                yanchor="bottom",
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
        margin=dict(l=1, r=1, b=1, t=75, pad=0),
        legend_orientation="h",
        legend=dict(x=0.22, y=-0.9),
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
        xaxis=dict(
            title="Frequency",
            gridcolor="#FFFFFF",
            showgrid=True,
            showline=True,
            linecolor="rgb(102, 102, 102)",
            tickfont_color="rgb(255, 255, 255)",
            showticklabels=True,
            dtick=200,
            ticks="outside",
            tickcolor="rgb(255, 255, 255)",
        ),
        yaxis=dict(title="Word", ticks="", gridcolor="#FFFFFF"),
        paper_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        font=dict(family="Raleway", color="#FFFFFF",),
        plot_bgcolor="rgba(255,255,255,0.9)",
        margin=dict(l=1, r=1, b=1, t=1, pad=0),
    )

    output = plot(dict(data=traces, layout=layout), config=config, output_type="div")

    return output


def sentiment_by_words():

    df = pd.read_csv("data/sentiment_by_keyword.csv")
    df = df.sort_values("Count")

    trace_positive = go.Scatter(
        x=df["Positive"],
        y=df["Word"],
        marker=dict(color="mediumseagreen", size=12),
        mode="markers",
        name="Positive",
    )

    trace_neutral = go.Scatter(
        x=df["Neutral"],
        y=df["Word"],
        marker=dict(color="orange", size=12),
        mode="markers",
        name="Neutral",
    )

    trace_negative = go.Scatter(
        x=df["Negative"],
        y=df["Word"],
        marker=dict(color="crimson", size=12),
        mode="markers",
        name="Negative",
    )

    traces = [trace_positive, trace_neutral, trace_negative]

    layout = go.Layout(
        # xaxis=dict(title="Sentiment Proportion (%)", gridcolor="#FFFFFF"),
        xaxis=dict(
            title="Sentiment Proportion (%)",
            gridcolor="#FFFFFF",
            showgrid=False,
            showline=True,
            linecolor="rgb(102, 102, 102)",
            tickfont_color="rgb(255, 255, 255)",
            showticklabels=True,
            dtick=10,
            ticks="outside",
            tickcolor="rgb(255, 255, 255)",
        ),
        yaxis=dict(title="Keyword", ticks="", gridcolor="#FFFFFF"),
        paper_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        font=dict(family="Raleway", color="#FFFFFF",),
        plot_bgcolor="rgba(255,255,255,0.9)",
        margin=dict(l=1, r=1, b=1, t=1, pad=0),
        width=1000,
        legend_orientation="h",
    )

    output = plot(dict(data=traces, layout=layout), config=config, output_type="div")

    return output


def cross_correlation():

    df_tweets = pd.read_csv("data/negative_proportions.csv")
    df_ftse = pd.read_csv("data/ftse.csv")
    normalised_articles = data.compute_normalised_news_article_count()

    trace_tweets = go.Scatter(x=df_tweets["Date"], y=df_tweets["Normalised"], name="No. of Negative Tweets")
    trace_article = go.Scatter(x=df_tweets["Date"], y=normalised_articles, name="No. of News Articles")
    trace_ftse = go.Scatter(x=df_ftse["Date"], y=df_ftse["Normalised Price"], name="FTSE Open Price")

    traces = [trace_tweets, trace_article, trace_ftse]

    layout = go.Layout(
        xaxis=dict(
            title="Date",
            gridcolor="#FFFFFF",
            showgrid=False,
            showline=True,
            linecolor="rgb(102, 102, 102)",
            tickfont_color="rgb(255, 255, 255)",
            showticklabels=True,
            # dtick=10,
            ticks="outside",
            tickcolor="rgb(255, 255, 255)",
        ),
        yaxis=dict(title="Normalised Ratio", ticks="", gridcolor="#FFFFFF"),
        paper_bgcolor="rgba(0,0,0,0)",
        template="plotly_dark",
        font=dict(family="Raleway", color="#FFFFFF",),
        plot_bgcolor="rgba(255,255,255,0.9)",
        margin=dict(l=1, r=1, b=1, t=1, pad=0),
        # width=1000,
        legend_orientation="h",
        legend=dict(orientation='h',yanchor='bottom',xanchor='center',y=-0.35,x=0.5)
    )

    output = plot(dict(data=traces, layout=layout), config=config, output_type="div")

    return output
