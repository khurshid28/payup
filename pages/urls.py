from django.contrib import admin
from django.urls import path

from pages import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate_pdfs_view/', views.generate_pdfs_view, name='generate_pdfs_view'),
]