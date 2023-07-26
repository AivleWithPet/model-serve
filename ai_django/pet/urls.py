from django.urls import path
from . import views

app_name = 'pet'

urlpatterns = [
    path('result', views.result, name='result'),
]