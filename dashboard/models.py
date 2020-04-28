from django.db import models
from datetime import date


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=100)
    date = models.DateField(("Date"), default=date.today)
    time = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    tweet = models.TextField()
    city = models.CharField(max_length=100)
    replies_count = models.IntegerField()
    retweets_count = models.IntegerField()
    likes_count = models.IntegerField()
    popular = models.BooleanField()
    verified = models.BooleanField()
    output = models.CharField(max_length=10)
    positive = models.DecimalField(max_digits=10, decimal_places=5)
    negative = models.DecimalField(max_digits=10, decimal_places=5)
    
    class Meta:
        ordering = ('date',)
    
    def __unicode__(self):
        return self.first

class Article(models.Model):
    article_id = models.TextField()
    date = models.DateField(("Date"), default=date.today)
    section = models.CharField(max_length=100)
    headline = models.TextField()
    url = models.TextField()
    article = models.TextField()
    
    class Meta:
        ordering = ('date',)
    
    def __unicode__(self):
        return self.first

class FTSE(models.Model):
    date = models.DateField(("Date"), default=date.today)
    open = models.FloatField()
    close = models.FloatField()
    low = models.FloatField()
    high = models.FloatField()
    volume = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('date',)
    
    def __unicode__(self):
        return self.first
    