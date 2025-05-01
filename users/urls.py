from django.urls import path
from . import views

urlpatterns=[
    path('user/', views.UserView.as_view(), name='login'),
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
]