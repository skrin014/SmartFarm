from django.urls import path, include
from numpy import delete
from myapp import views

urlpatterns = [
    path('', views.index),
    path('edit/', views.edit),
]