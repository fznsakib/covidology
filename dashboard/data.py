import pandas as pd

urls = {
    "confirmed": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "recovered": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
    "deaths": "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
}


def get_global():
    cases = []

    df = pd.read_csv(urls["confirmed"])
    cases.append(df.iloc[:, -1].sum())

    df = pd.read_csv(urls["recovered"])
    cases.append(df.iloc[:, -1].sum())

    df = pd.read_csv(urls["deaths"])
    cases.append(df.iloc[:, -1].sum())

    return cases


def get_top10():
    df_confirmed = pd.read_csv(urls["confirmed"])

    # Get top 10 largest by cases
    df_confirmed = df_confirmed.nlargest(10, df_confirmed.columns[-1])

    top10 = []
    top10_dict = {}

    current_date = df_confirmed.iloc[:, -1].name

    # Get country name and number of cases for each country
    for index, row in df_confirmed.iterrows():
        country = ""

        # If there is state named, add to country name
        if not str(row["Province/State"]) == "nan":
            country = str(row["Province/State"]) + ", "

        country += row["Country/Region"]
        cases = row[current_date]

        top10.append([country, cases])

    return top10
