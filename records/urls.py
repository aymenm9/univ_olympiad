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
    path('birth_certificate_confirm/<str:birth_number>/', views.BirthCertificateConfirm.as_view(), name='birth-certificate'),
    path('death_certificate_confirm/<str:death_number>/', views.DeathCertificateConfirm.as_view(), name='death-certificate'),
    path('statistics/', views.StatisticView.as_view(), name='statistics'),
    path('statistics/by_month/', views.MonthlyStatisticView.as_view(), name='statistics'),
    path('statistics_v2/', views.StatisticViewV2.as_view(), name='statistics'),
    path('public_birth_certificate/', views.PublicBirthCertificatePDf.as_view(), name='public-birth-certificate'),
    path('public_death_certificate/', views.PublicDeathCertificatePDf.as_view(), name='public-death-certificate'),
    path('burial_permit/', views.BurialPermitView.as_view(), name='list burial permit'),
    path('burial_permit_pdf/<str:death_number>/', views.BurialPermitPdfView.as_view(), name='burial permit detail'),
    path('burial_permit_confirm/<str:death_number>/', views.BurialPermitconfirmView.as_view(), name='burial permit confirm'),

    path('generate_death_ai/', views.AiView.as_view(), name='generate-death-ai'),
   
]