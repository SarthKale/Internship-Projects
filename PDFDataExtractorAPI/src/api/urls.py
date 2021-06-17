from django.urls import path
from .views import home, createSheet, convertToPDF

urlpatterns = [
    path('', home, name="home"),
    path('/createdata', createSheet, name="createSheet"),
    path('/convert', convertToPDF, name="convertPDF"),
]
