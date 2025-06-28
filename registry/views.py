import json
import os
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET

from core import settings
from entities.models import Patient, Visit, Doctor, SYMPTOMS_LIST, Symptom, Analysis
from .forms import VisitForm, PatientForm, DoctorForm, AnalysisForm
from django.contrib import messages
from authentication.forms import UserRegisterForm
from simple_history.utils import update_change_reason
import requests
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth

manager_permission = 'admin.manager_permission'
doctor_permission = 'admin.doctor_permission'


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации. Попробуйте снова.')
    else:
        form = UserRegisterForm()
    return render(request, 'registry/register_user.html', {'form': form})


@login_required
@permission_required(manager_permission, raise_exception=True)
def manage_patients(request):
    last_name = request.GET.get('last_name', '')
    first_name = request.GET.get('first_name', '')
    middle_name = request.GET.get('middle_name', '')
    date_of_birth = request.GET.get('date_of_birth', '')
    gender = request.GET.get('gender', '')
    phone_number = request.GET.get('phone_number', '')

    patients_list = Patient.objects.all()
    if not Patient.objects.exists():
        add_patient_url = reverse('add_patient')
        message = mark_safe(f"В настоящее время нет данных о пациентах  . <a href='{add_patient_url}'>Добавить пациента</a>.")
        messages.warning(request, message)
        return redirect('main')

    if last_name:
        patients_list = patients_list.filter(last_name__icontains=last_name)
    if first_name:
        patients_list = patients_list.filter(first_name__icontains=first_name)
    if middle_name:
        patients_list = patients_list.filter(middle_name__icontains=middle_name)
    if date_of_birth:
        start_date_str, end_date_str = date_of_birth.split(' — ')
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y')
        patients_list = patients_list.filter(date_of_birth__range=(start_date, end_date))
    if gender:
        patients_list = patients_list.filter(gender=gender)
    if phone_number:
        patients_list = patients_list.filter(phone_number__icontains=phone_number)

    if not patients_list:
        messages.warning(request, 'Пациенты, соответствующие введенным фильтрам, не найдены.')
        return redirect('manage_patients')

    per_page = patients_list.count() if any([last_name, first_name, middle_name, date_of_birth, gender, phone_number]) \
        else 10

    paginator = Paginator(patients_list, per_page)
    page_number = request.GET.get('page')
    try:
        patients = paginator.page(page_number)
    except PageNotAnInteger:
        patients = paginator.page(1)
    except EmptyPage:
        patients = paginator.page(paginator.num_pages)

    return render(request, 'registry/manage_patients.html', {'patients': patients})


@login_required
@permission_required(manager_permission)
def view_patient(request, pk):
    target_patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=target_patient)
        if form.is_valid():

            form.save()
            update_change_reason(target_patient, f"Updated by {request.user.username}")
            return render(request, 'registry/view_patient.html', {'patient': target_patient, 'form': form})

    else:
        form = PatientForm(instance=target_patient)

    return render(request, 'registry/view_patient.html', {'patient': target_patient, 'form': form})


@login_required
@permission_required(manager_permission, raise_exception=True)
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    patient.user = user
                    patient.save()
                    update_change_reason(patient, f"Created by {request.user.username}")
                    messages.success(request, 'Пациент успешно связан с аккаунтом!')
                    return redirect('manage_patients')
            else:
                patient.save()
                update_change_reason(patient, f"Created by {request.user.username}")
                messages.success(request, 'Пациент успешно добавлен!')
                return redirect('manage_patients')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            return render(request, 'registry/add_patient.html', {'form': form})
    else:
        form = PatientForm()
        return render(request, 'registry/add_patient.html', {'form': form})

@login_required
@permission_required(manager_permission, raise_exception=True)
def delete_patient(request, patient_id):
    target_patient = Patient.objects.get(id=patient_id)
    target_patient.delete()
    update_change_reason(view_patient, f"Deleted by {request.user.username}")
    messages.success(request, 'Пациент успешно удален!')
    return redirect('manage_patients')


@login_required
@permission_required(manager_permission, raise_exception=True)
def manage_doctors(request):
    last_name = request.GET.get('last_name', '')
    first_name = request.GET.get('first_name', '')
    middle_name = request.GET.get('middle_name', '')
    date_of_birth = request.GET.get('date_of_birth', '')
    gender = request.GET.get('gender', '')
    phone_number = request.GET.get('phone_number', '')
    specialty = request.GET.get('specialty', '')

    doctors_list = Doctor.objects.all()
    if not Doctor.objects.exists():
        add_doctor_url = reverse('add_doctor')
        message = mark_safe(f"В настоящее время нет данных о персонале. <a href='{add_doctor_url}'>Добавить врача</a>.")
        messages.warning(request, message)
        return redirect('main')

    if last_name:
        doctors_list = doctors_list.filter(last_name__icontains=last_name)
    if first_name:
        doctors_list = doctors_list.filter(first_name__icontains=first_name)
    if middle_name:
        doctors_list = doctors_list.filter(middle_name__icontains=middle_name)
    if date_of_birth:
        start_date_str, end_date_str = date_of_birth.split(' — ')
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y')
        doctors_list = doctors_list.filter(date_of_birth__range=(start_date, end_date))
    if gender:
        doctors_list = doctors_list.filter(gender=gender)
    if phone_number:
        doctors_list = doctors_list.filter(phone_number__icontains=phone_number)
    if specialty:
        doctors_list = doctors_list.filter(specialty=specialty)

    if not doctors_list:
        messages.warning(request, 'Врачи, соответствующие введенным фильтрам, не найдены.')
        return redirect('manage_doctors')

    per_page = doctors_list.count() if any([last_name, first_name, middle_name, date_of_birth, gender, phone_number, specialty]) \
        else 10

    paginator = Paginator(doctors_list, per_page)
    page_number = request.GET.get('page')
    try:
        doctors = paginator.page(page_number)
    except PageNotAnInteger:
        doctors = paginator.page(1)
    except EmptyPage:
        doctors = paginator.page(paginator.num_pages)

    return render(request, 'registry/manage_doctors.html', {'doctors': doctors})


@login_required
@permission_required(manager_permission, raise_exception=True)
def view_doctor(request, pk):
    target_doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=target_doctor)
        if form.is_valid():
            form.save()
            update_change_reason(target_doctor, f"Updated by {request.user.username}")
            return render(request, 'registry/view_doctor.html', {'doctor': target_doctor, 'form': form})
    else:
        form = DoctorForm(instance=target_doctor)
    return render(request, 'registry/view_doctor.html', {'doctor': target_doctor, 'form': form})


@login_required
@permission_required(manager_permission, raise_exception=True)
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            update_change_reason(doctor, f"Created by {request.user.username}")
            messages.success(request, 'Врач успешно добавлен!')
            return redirect('manage_doctors')
        else:
            return render(request, 'registry/add_doctor.html', {'form': form})
    else:
        form = DoctorForm()
        return render(request, 'registry/add_doctor.html', {'form': form})


@login_required
@permission_required(manager_permission, raise_exception=True)
def delete_doctor(request, doctor_id):
    target_doctor = Doctor.objects.get(id=doctor_id)
    target_doctor.delete()
    print(request.user.username)
    update_change_reason(target_doctor, f"Deleted by {request.user.username}")
    messages.success(request, 'Врач успешно удален!')
    return redirect('manage_doctors')


@login_required
@permission_required(doctor_permission, raise_exception=True)
def view_visit(request, pk):
    visit = get_object_or_404(Visit, id=pk)

    if request.method == 'POST':
        post_data = request.POST.copy()

        icd10_data = []
        try:
            if 'icd10_diagnosis' in request.POST:
                raw_data = request.POST.getlist('icd10_diagnosis')
                valid_data = [d for d in raw_data if d and d.strip() not in ['', '[]']]
                if valid_data:
                    first_valid = valid_data[0]
                    if isinstance(first_valid, str):
                        icd10_data = json.loads(first_valid)
                    else:
                        icd10_data = first_valid

            if not icd10_data and 'icd10_diagnosis' in post_data:
                if isinstance(post_data['icd10_diagnosis'], list):
                    icd10_data = post_data['icd10_diagnosis']

        except (json.JSONDecodeError, IndexError, AttributeError) as e:
            print(f"Error parsing ICD10 data: {e}")
            icd10_data = []

        if not isinstance(icd10_data, list):
            icd10_data = []

        post_data['icd10_diagnosis'] = json.dumps(icd10_data)

        form = VisitForm(post_data, instance=visit)

        if form.is_valid():
            visit = form.save(commit=False)
            visit.icd10_diagnosis = icd10_data

            symptoms = form.cleaned_data.get('symptoms')
            if symptoms:
                visit.symptoms.set(symptoms)

            visit.save()
            update_change_reason(visit, f"Updated by {request.user.username}")
            messages.success(request, 'Посещение успешно обновлено!')
            return redirect('manage_visits')

        print("Form errors:", form.errors)
        return render(request, 'registry/view_visit.html', {'form': form, 'visit': visit})

    else:
        form = VisitForm(instance=visit)
        return render(request, 'registry/view_visit.html', {'form': form, 'visit': visit})
@login_required
@permission_required(doctor_permission, raise_exception=True)
def manage_visits(request):
    patient = request.GET.get('patient', '')
    doctor = request.GET.get('doctor', '')
    symptoms = request.GET.get('symptoms', '')
    examination = request.GET.get('examination', '')
    diagnosis = request.GET.get('diagnosis', '')
    visit_date = request.GET.get('visit_date', '')

    visits_list = Visit.objects.all()

    if not Visit.objects.exists():
        add_visit_url = reverse('add_visit')
        message = mark_safe(f"В настоящее время журнал посещений пуст. <a href='{add_visit_url}'>Добавить посещение</a>.")
        messages.warning(request, message)
        return redirect('main')

    if patient:
        visits_list = visits_list.filter(patient__last_name__icontains=patient)
    if doctor:
        visits_list = visits_list.filter(doctor__last_name__icontains=doctor)
    if visit_date:
        start_date_str, end_date_str = visit_date.split(' — ')
        start_date = datetime.strptime(start_date_str, '%d.%m.%Y %H:%M')
        end_date = datetime.strptime(end_date_str, '%d.%m.%Y %H:%M')
        visits_list = visits_list.filter(visit_date__range=(start_date, end_date))
    if symptoms:
        visits_list = visits_list.filter(symptoms__icontains=symptoms)
    if examination:
        visits_list = visits_list.filter(examination__icontains=examination)
    if diagnosis:
        visits_list = visits_list.filter(diagnosis__icontains=diagnosis)

    if not visits_list.exists():
        messages.warning(request, 'Посещения, соответствующие введенным фильтрам, не найдены.')
        return redirect('manage_visits')

    per_page = visits_list.count() if any([patient, doctor, symptoms, examination, diagnosis, visit_date]) else 10

    paginator = Paginator(visits_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        visits = paginator.page(page_number)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(paginator.num_pages)

    return render(request, 'registry/manage_visits.html', {'visits': visits})

def get_symptoms(request):
    term = request.GET.get('term', '')
    symptoms = Symptom.objects.filter(name__icontains=term)
    results = [{'id': symptom.id, 'text': symptom.name} for symptom in symptoms]
    return JsonResponse(results, safe=False)


@login_required
@permission_required(doctor_permission, raise_exception=True)
def add_visit(request):
    if request.method == 'POST':
        print("Raw POST data:", request.POST)

        patient_raw = request.POST.get('patient')
        print(f"Raw patient from POST: {patient_raw}")
        icd10_raw = request.POST.getlist('icd10_diagnosis')[0]
        print(f"Raw ICD10 from POST: {icd10_raw}")

        post_data = request.POST.copy()

        form = VisitForm(post_data)

        if form.is_valid():
            visit = form.save(commit=False)

            if icd10_raw and icd10_raw != '[]':
                try:
                    visit.icd10_diagnosis = json.loads(icd10_raw)
                    print(f"Parsed ICD10: {visit.icd10_diagnosis}")
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    visit.icd10_diagnosis = []
            else:
                visit.icd10_diagnosis = []

            visit.save()
            form.save_m2m()

            messages.success(request, 'Посещение успешно добавлено!')
            return redirect('manage_visits')

        print("Form errors:", form.errors)
        return render(request, 'registry/add_visit.html', {'form': form})

    form = VisitForm()
    return render(request, 'registry/add_visit.html', {'form': form})


@login_required
@permission_required(doctor_permission, raise_exception=True)
def delete_visit(request, visit_id):
    target_visit = Visit.objects.get(id=visit_id)
    target_visit.delete()
    update_change_reason(target_visit, f"Deleted by {request.user.username}")
    messages.success(request, 'Посещение успешно удалено!')
    return redirect('manage_visits')



@login_required
@permission_required('doctor_permission', raise_exception=True)
def add_analysis(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.save()

            messages.success(request, 'Анализ успешно добавлен!')
            return redirect('manage_analyses')
        else:
            return render(request, 'registry/add_analysis.html', {'form': form})
    else:
        form = AnalysisForm()

    return render(request, 'registry/add_analysis.html', {'form': form})


@login_required
@permission_required('doctor_permission', raise_exception=True)
def manage_analyses(request):
    patient_name = request.GET.get('patient_name', '').strip()
    test_name = request.GET.get('test_name', '').strip()
    date_range = request.GET.get('date', '').strip()
    status = request.GET.get('status', '').strip()

    analyses_list = Analysis.objects.select_related('patient').all()

    if not analyses_list.exists():
        add_analysis_url = reverse('add_analysis')
        message = mark_safe(f"В настоящее время нет данных об анализах. <a href='{add_analysis_url}'>Добавить анализ</a>.")
        messages.warning(request, message)
        return redirect('main')

    if patient_name:
        analyses_list = analyses_list.filter(
            patient__first_name__icontains=patient_name
        ) | analyses_list.filter(
            patient__last_name__icontains=patient_name
        )

    if test_name:
        analyses_list = analyses_list.filter(test_name__icontains=test_name)

    if date_range:
        try:
            start_str, end_str = date_range.split(' — ')
            start_date = datetime.strptime(start_str.strip(), '%d.%m.%Y')
            end_date = datetime.strptime(end_str.strip(), '%d.%m.%Y')
            analyses_list = analyses_list.filter(date__range=(start_date, end_date))
        except (ValueError, IndexError):
            messages.error(request, 'Неверный формат даты. Используйте "дд.мм.гггг — дд.мм.гггг".')

    if status:
        analyses_list = analyses_list.filter(status=status)

    if not analyses_list.exists():
        messages.warning(request, 'Анализы, соответствующие введённым фильтрам, не найдены.')
        return redirect('manage_analyses')

    has_filters = any([patient_name, test_name, date_range, status])
    per_page = analyses_list.count() if has_filters else 10

    paginator = Paginator(analyses_list.order_by('-date'), per_page)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'registry/manage_analyses.html', {'page_obj': page_obj})

def download_analysis(request, analysis_id):
    analysis_instance = get_object_or_404(Analysis, id=analysis_id)

    original_file_path = analysis_instance.analysis_file.path if analysis_instance.analysis_file else None
    if original_file_path and os.path.exists(original_file_path):
        with open(original_file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(original_file_path)}"'
            return response

    return HttpResponse('Файл не найден', status=404)

@login_required
@permission_required('doctor_permission', raise_exception=True)
def view_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)

    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES, instance=analysis)
        if form.is_valid():
            form.save()
            update_change_reason(analysis, f"Updated by {request.user.username}")
            messages.success(request, 'Анализ успешно обновлён!')
            return redirect('view_analysis', analysis_id=analysis.id)
    else:
        form = AnalysisForm(instance=analysis)

    return render(request, 'registry/view_analysis.html', {
        'analysis': analysis,
        'form': form,
    })

@login_required
@permission_required('doctor_permission', raise_exception=True)
def delete_analysis(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)
    username = request.user.username
    analysis.delete()
    update_change_reason(analysis, f"Deleted by {username}")
    messages.success(request, 'Анализ успешно удалён!')
    return redirect('manage_analyses')

def get_doctors(request):
    term = request.GET.get('term', '')
    doctors = Doctor.objects.filter(name__icontains=term)
    results = [{'id': doctor.id, 'name': doctor.name} for doctor in doctors]
    return JsonResponse(results, safe=False)



def get_icd_access_token():
    url = "https://icdaccessmanagement.who.int/connect/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': settings.ICD_CLIENT_ID,
        'client_secret': settings.ICD_CLIENT_SECRET,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get('access_token')

def icd10_search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'results': []})

    token = get_icd_access_token()
    search_url = "https://id.who.int/icd/release/11/2025-01/mms/search"
    params = {
        'q': query,
        'useFlexisearch': 'true',
        'flatResults': 'true',
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Accept-Language': 'ru',
        'API-Version': 'v2',
    }

    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        return JsonResponse({'results': [], 'error': str(e)})

    data = response.json()
    results = []
    for item in data.get('destinationEntities', []):
        entity_id = item.get('id', '')
        entity_id_short = entity_id.split('/')[-1] if '/' in entity_id else entity_id
        title = item.get('title', '').replace('<[^>]+>', '')
        code = item.get('theCode', '')
        chapter = item.get('chapter', '')

        results.append({
            'id': code,
            'text': f"{code} — {title}",
            'entity_id': entity_id_short,
            'chapter': chapter,
            'url': f"https://icd.who.int/browse/2025-01/mms/ru#{entity_id_short}"
        })

    return JsonResponse({'results': results})

def icd10_get_by_entity(request):
    entity_id = request.GET.get('entity_id')
    if not entity_id:
        return JsonResponse({'error': 'entity_id required'}, status=400)

    token = get_icd_access_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Accept-Language': 'ru',
        'API-Version': 'v2',
    }

    try:
        url = f"https://id.who.int/icd/entity/{entity_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        result = {
            'id': data.get('theCode', ''),
            'text': f"{data.get('theCode', '')} — {data.get('title', {}).get('@value', '')}",
            'entity_id': entity_id,
        }
        return JsonResponse({'results': [result]})

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
