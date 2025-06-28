import csv
from collections import Counter

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Patient, Visit, Symptom
from django.db import models


def main(request):
    return render(request, 'main/main.html')


def patient_statistics(request):
    total_patients = Patient.count_patients()
    age_groups = Patient.patients_by_age_group()
    gender_distribution = Patient.count_patients_by_gender()

    visits_list = Visit.objects.all()

    symptoms_count = visits_list.values('symptoms').annotate(count=Count('symptoms')).order_by('-count')

    symptom_ids = [item['symptoms'] for item in symptoms_count]
    symptoms = Symptom.objects.filter(id__in=symptom_ids)

    all_diagnoses = []
    for visit in visits_list:
        diag_list = visit.icd10_diagnosis or []
        for diag in diag_list:
            all_diagnoses.append(diag.get('description', 'Неизвестно'))
    diagnosis_counter = Counter(all_diagnoses)
    diagnosis_count = sorted(
        [{'diagnosis': code, 'count': count} for code, count in diagnosis_counter.items()],
        key=lambda x: x['count'], reverse=True
    )

    date_visit_count = (
        visits_list
        .values('visit_date__date')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    return render(request, 'analytics/patient_statistics.html', {
        'total_patients': total_patients,
        'age_groups': age_groups,
        'gender_distribution': gender_distribution,
        'visits_count': visits_list.count(),
        'symptoms_count': symptoms_count,
        'symptoms': symptoms,  # Передаем симптомы с их названиями
        'diagnosis_count': diagnosis_count,
        'date_visit_count': date_visit_count,
    })


def export_patient_statistics(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_statistics.csv"'

    response.charset = 'utf-8-sig'

    writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Имя', 'Фамилия', 'Отчество', 'Дата рождения', 'Пол', 'Возраст'])

    patients = Patient.objects.all()
    for patient in patients:
        writer.writerow([patient.first_name, patient.last_name, patient.middle_name, patient.date_of_birth,
                         patient.get_gender_display(), patient.age])

    return response


def export_visit_statistics(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="visit_statistics.csv"'
    response.charset = 'utf-8-sig'

    writer = csv.writer(response, delimiter=';', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['Дата посещения', 'Пациент', 'Симптомы', 'Диагнозы'])

    visits = Visit.objects.select_related('patient').all().order_by('visit_date')

    for visit in visits:
        if hasattr(visit, 'symptoms') and hasattr(visit.symptoms, 'all'):
            symptoms = ', '.join(str(s) for s in visit.symptoms.all())
        else:
            symptoms = visit.symptoms if hasattr(visit, 'symptoms') else ''

        diagnoses_list = []
        if visit.icd10_diagnosis:
            for diag in visit.icd10_diagnosis:
                desc = diag.get('description') or diag.get('code') or 'Неизвестно'
                diagnoses_list.append(desc)
        diagnoses = ', '.join(diagnoses_list)

        writer.writerow([
            visit.visit_date.strftime('%d.%m.%Y') if visit.visit_date else '',
            f"{visit.patient.first_name} {visit.patient.last_name}" if visit.patient else '',
            symptoms,
            diagnoses,
        ])

    return response
