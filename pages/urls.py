from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test_error', views.test_error, name='test_error'),
]