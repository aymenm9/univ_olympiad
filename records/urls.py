from django.urls import path
from . import views

urlpatterns=[
    path('birth/', views.BirthRecordView.as_view(), name='birth-record'),
    path('death/', views.DeathRecordView.as_view(), name='death-record'),
    path('birth/<int:birth_number>/', views.BirthRecordDetailView.as_view(), name='birth-record-detail'),
    path('death/<int:birth_number>/', views.DeathRecordDetailView.as_view(), name='death-record-detail'),
    path('generate_death_ai/', views.AiView.as_view(), name='generate-death-ai'),
]