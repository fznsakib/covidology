import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.graph_objects as go
from dashboard.models import Tweet

def city_sentiment():

    df = pd.read_csv('data/sentiment_ratios.csv')
    
    # Create graph
    x_data = df["Date"]
    y_data = df["London"]
    trace_london = Scatter(
        x=x_data,
        y=y_data,
        mode="lines",
        name="sentiment_by_city",
        opacity=0.8,
        marker_color="green",
    )

    data = [trace_london]
    
    layout = go.Layout(
        # title='Win Probability Matrix',
        xaxis=dict(title='Date', ticks=''),
        yaxis=dict(title='Sentiment Log Ratio', ticks=''),
        # height=750
    )

    output = plot(dict(data=data, layout=layout), output_type="div")

    return output
