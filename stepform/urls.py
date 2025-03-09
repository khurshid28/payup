from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # Contract turi yuboriladi. Mikrokredit/Mikroqarz/Sugurta
    path('step_contract/<str:credit_type>/', views.step_contract, name='step_contract'),
    path('step_customer/', views.step_customer, name='step_customer'),
    path('step_pledge/', views.step_pledge, name='step_pledge'),
    path('done/', views.done, name='done'),

    # OPERATOR
    path('operator_list/', views.operator_list, name='operator_list'),

    # MODERATOR
    path('moderator_list/', views.moderator_list, name='moderator_list'),
    path('moderator_form/<int:pk>/', views.moderator_form, name='moderator_form'),

    # DIREKTOR
    path('direktor_list/', views.direktor_list, name='direktor_list'),
    path('direktor_form/<int:pk>/', views.direktor_form, name='direktor_form'),

    # KREDITLASH LOAN
    path('loan_head_list/', views.loan_head_list, name='loan_head_list'),
    path('loan_head_form/<int:pk>/', views.loan_head_form, name='loan_head_form'),

    # MONITORING LOAN
    path('monitoring_head_list/', views.monitoring_head_list, name='monitoring_head_list'),
    path('monitoring_head_form/<int:pk>/', views.monitoring_head_form, name='monitoring_head_form'),
]
