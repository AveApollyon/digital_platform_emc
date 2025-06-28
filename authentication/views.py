from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from authentication.forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
            if user is not None:
                login(request, user)
                messages.success(request, 'Ваш аккаунт был успешно создан!')
                return redirect('main')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = UserRegisterForm()
    return render(request, 'authentication/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    visits_list = None
    analyses_list = None

    if hasattr(user, 'patient'):
        visits_list = user.patient.visit_set.prefetch_related(
            Prefetch('symptoms', to_attr='symptom_list')
        )
        analyses_list = user.patient.analyses.all()
    elif hasattr(user, 'doctor'):
        visits_list = user.doctor.visit_set.prefetch_related(
            Prefetch('symptoms', to_attr='symptom_list')
        )

    visit_date = request.GET.get('visit_date', '')
    patient = request.GET.get('patient', '')
    doctor = request.GET.get('doctor', '')
    doctor_specialty = request.GET.get('doctor_specialty', '')
    symptoms = request.GET.get('symptoms', '')
    examination = request.GET.get('examination', '')
    diagnosis = request.GET.get('diagnosis', '')

    if visit_date:
        start_date_str, end_date_str = visit_date.split(' — ')
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y %H:%M')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y %H:%M')
        visits_list = visits_list.filter(visit_date__range=(start_date, end_date))

    if patient:
        visits_list = visits_list.filter(patient__last_name__icontains=patient)
    if doctor:
        visits_list = visits_list.filter(doctor__last_name__icontains=doctor)
    if doctor_specialty:
        visits_list = visits_list.filter(doctor__specialty=doctor_specialty)
    if symptoms:
        visits_list = visits_list.filter(symptoms__name__icontains=symptoms)
    if examination:
        visits_list = visits_list.filter(examination__icontains=examination)
    if diagnosis:
        visits_list = visits_list.filter(diagnosis__icontains=diagnosis)

    test_name = request.GET.get('test_name', '')
    status = request.GET.get('status', '')
    if test_name:
        analyses_list = analyses_list.filter(test_name__icontains=test_name)
    if status:
        analyses_list = analyses_list.filter(status=status)

    per_page = visits_list.count() if any([visit_date, patient, doctor, doctor_specialty, symptoms, examination, diagnosis]) else 2
    paginator = Paginator(visits_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        visits = paginator.page(page_number)
        for visit in visits:
            if hasattr(visit, 'symptom_list'):
                visit.symptoms_text = ', '.join([s.name for s in visit.symptom_list])
            else:
                visit.symptoms_text = ''
    except PageNotAnInteger:
        visits = paginator.page(1)
        for visit in visits:
            if hasattr(visit, 'symptom_list'):
                visit.symptoms_text = ', '.join([s.name for s in visit.symptom_list])
            else:
                visit.symptoms_text = ''
    except EmptyPage:
        visits = paginator.page(paginator.num_pages)
        for visit in visits:
            if hasattr(visit, 'symptom_list'):
                visit.symptoms_text = ', '.join([s.name for s in visit.symptom_list])
            else:
                visit.symptoms_text = ''

    analyses_per_page = analyses_list.count() if any([test_name, status]) else 5
    analyses_paginator = Paginator(analyses_list, analyses_per_page)
    analysis_page_number = request.GET.get('analysis_page', 1)
    try:
        analyses = analyses_paginator.page(analysis_page_number)
    except PageNotAnInteger:
        analyses = analyses_paginator.page(1)
    except EmptyPage:
        analyses = analyses_paginator.page(analyses_paginator.num_pages)

    return render(request, 'authentication/profile.html', {'user': user, 'visits': visits, 'analyses': analyses})
