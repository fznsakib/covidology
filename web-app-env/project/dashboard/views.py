from django.shortcuts import render
from plotly.offline import plot
from plotly.graph_objs import Scatter

import copy


def dashboard(request):
    x_data = [0, 1, 2, 3]
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
