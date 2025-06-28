from django.urls import path
from registry import views

urlpatterns = [
    path('manage_patients/', views.manage_patients, name='manage_patients'),
    path('view_patient/<int:pk>/', views.view_patient, name='view_patient'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('manage_doctors/', views.manage_doctors, name='manage_doctors'),
    path('view_doctor/<int:pk>/', views.view_doctor, name='view_doctor'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('manage_visits/', views.manage_visits, name='manage_visits'),
    path('view_visit/<int:pk>/', views.view_visit, name='view_visit'),
    path('add_visit/', views.add_visit, name='add_visit'),
    path('delete_visit/<int:visit_id>/', views.delete_visit, name='delete_visit'),
    path('get_symptoms/', views.get_symptoms, name='get_symptoms'),
    path('add_analysis/', views.add_analysis, name='add_analysis'),
    path('manage_analyses/', views.manage_analyses, name='manage_analyses'),
    path('view_analysis/<int:analysis_id>/', views.view_analysis, name='view_analysis'),
    path('delete_analysis/<int:analysis_id>/', views.delete_analysis, name='delete_analysis'),
    path('download_analysis/<int:analysis_id>/', views.download_analysis, name='download_analysis'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('icd10/search/', views.icd10_search, name='icd10_search'),
    path('icd10/search_by_id/', views.icd10_get_by_entity, name='icd10_search_by_id')
]
