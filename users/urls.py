from django.urls import path
from . import views

urlpatterns=[
    path('user/', views.UserView.as_view(), name='login'),
    path('hospital/', views.CreateHospitalView.as_view(), name='create_hospital_and_his_admin'),
]