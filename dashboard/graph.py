import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dashboard.data as data
import datetime
from plotly.offline import plot
from plotly.graph_objs import Scatter
from dashboard.models import Tweet

config = {"displaylogo": False, "scrollZoom": True, "responsive": True}

def city_sentiment_map():
    df = pd.read_csv("data/negative_proportions.csv")
    df = df.set_index("Date")

    list_of_cities = df.columns
    list_of_cities = list_of_cities[1:-1]

    #Store Lat and Long values
    lat = {}

    lat['London'] = 51.51
    lat['Bristol'] = 51.45
    lat['Manchester'] = 53.48
    lat['Liverpool'] = 53.40
    lat['Birmingham'] = 52.49
    lat['Leeds'] = 53.80
    lat['Oxford'] = 51.75
    lat['Glasgow'] = 55.86
    lat['Dublin'] = 53.35
    lat['Cardiff'] = 51.48

    long = {}

    long['London'] = -0.12
    long['Bristol'] = -2.59
    long['Manchester'] = -2.24
    long['Liverpool'] = -2.98
    long['Birmingham'] = -1.90
    long['Leeds'] = -1.55
    long['Oxford'] = -1.26
    long['Glasgow'] = -4.25
    long['Dublin'] = -6.27
    long['Cardiff'] = -3.18

    city_dataframe = {}
    for city in list_of_cities:
        city_dataframe[city] = pd.DataFrame(
            {'Date': df[city].index,
             'Location':df[city].name,
             'Proportion of negative tweets':df[city].values,
             'Lat': lat[city],
             'Long': long[city]}
        )

    data = pd.concat(city_dataframe.values())
    data['Size'] = 25

    fig = px.scatter_mapbox(
        data,
        lat="Lat",
        lon="Long",
        color="Proportion of negative tweets",
        size="Size",
        color_continuous_scale=px.colors.diverging.Geyser,
        size_max=25,
        zoom=5,
        hover_name="Location",
        mapbox_style="carto-darkmatter",
        animation_frame="Date",
        animation_group="Location",
        range_color=[0.0,1.0]
    )

    config = {'responsive': True}

    fig.update_layout(
        # autosize=True,
        # width=70%,
        height=650,
        margin=dict(l=30, r=130, b=10, t=10, pad=4),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Raleway", color="#FFFFFF"),
    )

    output = plot(fig, output_type="div", config=config)
        
    return output

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
        # autosize=True,
        # width=70%,
        height=650,
        margin=dict(l=30, r=130, b=10, t=10, pad=4),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Raleway", color="#FFFFFF"),
    )

    config = {'responsive': True}

    output = plot(fig, output_type="div",config=config)

    # Convert date format and return to display on page
    latest_date = datetime.datetime.strptime(latest_date, "%m/%d/%y").strftime("%d/%m/%y")

    return output, latest_date

"""
Line graph showing number of tweets for each sentiment over the time period
x = dates
y = number of tweets

Data in num_tweets_by_sentiment.csv
"""
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
    # plot(dict(data=traces, layout=layout), config=config, filename='num_tweets.html', output_type='file',include_plotlyjs=True)

    return output


"""
Bar graph showing top 20 most used words in tweets collected
x = count
y = word

Data in top_words.csv (There's ~1700 words in this, ordered by count)

"""
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


"""
Dot plot showing keywords and the proportion of their tweets found showing each sentiment
x = proportion
y = keyword

Data in sentiment_by_keyword.csv

"""
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
        # width=1000,
        legend_orientation="h",
    )

    output = plot(dict(data=traces, layout=layout), config=config, output_type="div")

    return output


def cross_correlation():

    data.compute_normalised_news_article_count()

    df_tweets = pd.read_csv("data/num_tweets_by_sentiment.csv")
    df_ftse = pd.read_csv("data/ftse.csv")
    df_articles = pd.read_csv("data/news_normalised.csv")
    df_cases = pd.read_csv("data/cases_normalised.csv")

    trace_tweets = go.Scatter(x=df_tweets["Date"], y=df_tweets["Normalised Negative"], name="No. of Negative Tweets")
    trace_ftse = go.Scatter(x=df_ftse["Date"], y=df_ftse["Normalised Price"], name="FTSE Open Price")
    trace_article = go.Scatter(x=df_tweets["Date"], y=df_articles["Normalised Count"], name="No. of News Articles")
    trace_cases = go.Scatter(x=df_cases["Date"], y=df_cases["Normalised"], name="No. of COVID-19 Cases", line=dict(color='slategray'))

    traces = [trace_tweets, trace_article, trace_ftse, trace_cases]

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
        yaxis=dict(title="Normalised Value", ticks="", gridcolor="#FFFFFF"),
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
