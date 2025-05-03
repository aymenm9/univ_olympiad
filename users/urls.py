from django.urls import path
from . import views

urlpatterns=[
    path('user/', views.UserView.as_view(), name='login'),
    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('hospital/', views.CreateHospitalView.as_view(), name='create_hospital_and_his_admin'),
    path('apc/', views.CreateAPCView.as_view(), name='create_apc_and_his_admin'),
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
]