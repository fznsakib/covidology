from django.urls import path
from corona_app import views

urlpatterns = [
    path('', views.corona_app, name='corona_app'),
]
