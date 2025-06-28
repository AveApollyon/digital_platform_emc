from django.urls import path
from entities import views

urlpatterns = [
    path('', views.main, name='main'),
    path('patient_statistics/', views.patient_statistics, name='patient_statistics'),
    path('export_patient_statistics/', views.export_patient_statistics, name='export_patient_statistics'),
    path('export_visit_statistics/', views.export_visit_statistics, name='export_visit_statistics'),

]
