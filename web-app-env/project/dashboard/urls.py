from django.urls import path
from dashboard import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("map/", views.map, name="map"),
]
