from django.urls import path
from . import views

urlpatterns=[
    path('birth/', views.BirthRecordView.as_view(), name='birth-record'),
    path('death/', views.DeathRecordView.as_view(), name='death-record'),
    path('birth/<int:nuber_of_birth>/', views.BirthRecordDetailView.as_view(), name='birth-record-detail'),
    path('death/<int:nuber_of_birth>/', views.DeathRecordDetailView.as_view(), name='death-record-detail'),
    path('death_certificate/<int:nuber_of_birth>/', views.Death_certificate.as_view(), name='death-record-detail'),
    path('birth_certificate/<int:nuber_of_birth>/', views.Birth_certificate.as_view(), name='birth-record-detail'),
]