from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('verifyPoly/', views.verifyPoly),
    path('numberPoly/', views.numberPoly),
    path('startIteration/', views.startIteration),
    path('checkIteration/', views.checkIterationStatus),
    path('matrixPoly/', views.matrixPoly),
    path('csvPoly/', views.csvPoly)
]