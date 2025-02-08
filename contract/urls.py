from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # Mikroqarz
    path('mikroqarz_list/', views.mikroqarz_list, name='mikroqarz_list'),
    path('mikroqarz_detail/<int:pk>/', views.mikroqarz_detail, name='mikroqarz_detail'),
    path('mikroqarz_form/', views.mikroqarz_form, name='mikroqarz_form'),

    # Mikrokredit
    path('mikrokredit_form/', views.mikrokredit_form, name='mikrokredit_form'),

    path('moderator_list/', views.moderator_list, name='moderator_list'),
    path('moderator_form/<int:pk>/', views.moderator_form, name='moderator_form'),
    path('direktor_list/', views.direktor_list, name='direktor_list'),
    path('direktor_form/<int:document_id>/', views.direktor_form, name='direktor_form'),

    path('document_detail/<uuid:unique_identifier>/', views.document_detail, name='document_detail'),

    # path('create_contract/', views.CreateContract.as_view(), name='create_contract'),
    path('create_contract_doc/', views.CreateContractDoc.as_view(), name='create_contract_doc'),
]
