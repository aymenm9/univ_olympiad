from django.urls import path
from . import views

urlpatterns=[
    path('birth/', views.BirthRecordView.as_view(), name='birth-record'),
    path('death/', views.DeathRecordView.as_view(), name='death-record'),
    path('birth/<str:birth_number>/', views.BirthRecordDetailView.as_view(), name='birth-record-detail'),
    path('death/<str:death_number>/', views.DeathRecordDetailView.as_view(), name='death-record-detail'),
    path('birth_certificate_pdf/<str:birth_number>/', views.BirthCertificatePDF.as_view(), name='generate-birth-pdf'),
    path('death_certificate_pdf/<str:death_number>/', views.DeathCertificatePDf.as_view(), name='generate-death-pdf'),
    path('birth_certificate/', views.BirthCertificateView.as_view(), name='birth-certificate'),
    path('death_certificate/', views.DeathCertificateView.as_view(), name='death-certificate'),
    path('birth_certificate/<str:birth_number>/', views.BirthCertificateDetailView.as_view(), name='birth-certificate'),
    path('death_certificate/<str:death_number>/', views.DeathCertificateDetailView.as_view(), name='death-certificate'),
    path('statistics/', views.StatisticView.as_view(), name='statistics'),
    path('statistics_v2/', views.StatisticViewV2.as_view(), name='statistics'),


    path('generate_death_ai/', views.AiView.as_view(), name='generate-death-ai'),
   
]