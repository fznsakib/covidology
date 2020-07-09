<p align="center">
  <img src="https://user-images.githubusercontent.com/15062683/86980273-7924d900-c194-11ea-9cb4-1eb476ccf450.png" alt="covidology" width=500>
</p>

---

The goal of this project was to perform the analysis of the geographic sentiment distribution related to the COVID-19 pandemic specifically in the UK. To achieve this, a machine learning model in the form of an SVM, pre-trained on the [Sentiment140](https://www.kaggle.com/kazanova/sentiment140) dataset, was created for the classification of sentiment. Word2Vec was used to learn vector representations of individual words, helping to classify texts as negative, positive or neutral. The model was used to perform sentiment classification on a self-curated dataset of ~29000 tweets related to COVID-19.

<p align="center">
  <img src="https://user-images.githubusercontent.com/15062683/87018549-77820200-c1e2-11ea-99a8-2ab360b2adbc.png" alt="heatmap" width=700>
</p>

The evaluation of the sentiment analysis, and the model itself, is presented using a Django-based web application which can be viewed at [covidology.uk](covidology.uk).

This work was created as part of a group project for the *Applied Data Science* Unit at the University of Bristol.

**Team**: [Ellie Begbie](https://github.com/elliebegbie), [Andrew Corrigan](https://github.com/acorrigan64),  [Leechay Moran-Allen](https://github.com/aSpikyOreo), [Mark Ergus Nicholl](https://github.com/MarkErgusNicholl), [Arabella Peake](https://github.com/arabellapeake) and [Faizaan Sakib](https://github.com/fznsakib)

## Technologies

The dashboard involved the use of the following technologies:

- Python/Django
- Bootstrap/HTML/CSS/JS
- SQLite
- Pandas
- Plotly
- Heroku
- Cloudflare

## Data

Twitter was chosen as the main source of data for analysis. A total of 28876 tweets were collected, originating from 10 different UK cities to help obtain a geographical understanding of sentiment.

After the sentiment analysis of the tweets was carried out, it was essential that there was a reference point which could be used to evaluate the performance of the model. There does not exist a labelled dataset based on sentiment analysis, in relation to COVID-19. Thus, in addition to the Twitter data, a number of datasets are gathered to be used as sources of ground truth that can help to verify the predictions of a sentiment analysis model. They include:

1. COVID-19 Infection Cases
2. FTSE100 Market Prices
3. UK-based news articles relating to COVID-19

The data for all sources mentioned above, including the tweets, were collected within a 3 month time-frame between 25/12/2019 to 25/03/2020. 

## Results

The classification of the tweets showed an expected rise in negative sentiment over time, coinciding with the particular events such as the initial confirmed case and death caused by COVID-19 in the UK, along with the announcement of the nationwide lockdown.

<p align="center">
  <img src="https://user-images.githubusercontent.com/15062683/87017383-f2e2b400-c1e0-11ea-81ec-24ad7c01c648.jpg" alt="tweets sentiment" width=500>
</p>

In order to assess the performance of the model, its results had to be validated against trusted secondary sources of sentiment which would also be related to COVID-19. This is achieved by examining the correlation between the results of the sentiment analysis, and the other sources of data as outlined above. By normalising the daily frequency of tweets classified as negative by the model, along with three additional variables, it was possible to perform a time series cross-correlation. As shown by the graph below, the sentiment analysis of the tweets correlate strongly with the other data points. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/15062683/87018190-f75b9c80-c1e1-11ea-8713-e183c5767c67.jpg" alt="correlation" width=500>
</p>

# Web Development Setup

Python version: 3.6.8

To continue developing in virtualenv: `source web-app-env/bin/activate` and  `deactivate` to leave virtualenv

To run django application: `python manage.py runserver`

All required packages are listed with `requirements.txt` 
