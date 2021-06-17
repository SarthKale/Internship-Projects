from django.urls import path
from .views import createTable, home, createSheet, convertToPDF

urlpatterns = [
    path('', home, name="home"),
    path('/convert', convertToPDF, name="convertPDF"),
    path('/show', createTable, name="createTable"),
]
