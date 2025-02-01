from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('mikroqarz_list/', views.mikroqarz_list, name='mikroqarz_list'),
    path('mikroqarz_create/', views.mikroqarz_form, name='mikroqarz_form'),
    path('create_contract/', views.CreateContract.as_view(), name='create_contract'),
]