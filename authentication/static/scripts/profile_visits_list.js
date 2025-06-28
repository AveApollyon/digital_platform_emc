const visitListBody = document.getElementById('visit-list-body');

document.addEventListener("DOMContentLoaded", function() {
    const filterButton = document.getElementById('filter-visits');

    filterButton.addEventListener('click', function() {
        const visit_date = document.getElementById('visit_date').value;
        const patient = document.getElementById('patient') ? document.getElementById('patient').value : '';
        const doctor = document.getElementById('doctor') ? document.getElementById('doctor').value : '';
        const doctor_specialty = document.getElementById('doctor_specialty') ? document.getElementById('doctor_specialty').value : '';
        const symptoms = document.getElementById('symptoms').value;
        const examination = document.getElementById('examination').value;
        const diagnosis = document.getElementById('diagnosis').value;
        const prescriptions = document.getElementById('prescriptions').value;



        // Формирование URL с параметрами фильтрации
        const url = new URL(window.location.href);
        url.searchParams.set('visit_date', visit_date);
        if (patient) {
            url.searchParams.set('patient', patient);
        }
        if (doctor) {
            url.searchParams.set('doctor', doctor);
        }
        if (doctor_specialty) {
            url.searchParams.set('doctor_specialty', doctor_specialty);
        }
        url.searchParams.set('symptoms', symptoms);
        url.searchParams.set('examination', examination);
        url.searchParams.set('diagnosis', diagnosis);
        url.searchParams.set('prescriptions', prescriptions);

        // Переход на страницу с примененными фильтрами
        window.location.href = url.href;
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById('visit_date').value = urlParams.get('visit_date') || '';
    const patientInput = document.getElementById('patient');
    if (patientInput) {
        patientInput.value = urlParams.get('patient') || '';
    }
    const doctorInput = document.getElementById('doctor');
    if (doctorInput) {
        doctorInput.value = urlParams.get('doctor') || '';
    }
    const doctorSpecialtyInput = document.getElementById('doctor_specialty');
    if (doctorSpecialtyInput) {
        doctorSpecialtyInput.value = urlParams.get('doctor_specialty') || '';
    }
    document.getElementById('symptoms').value = urlParams.get('symptoms') || '';
    document.getElementById('examination').value = urlParams.get('examination') || '';
    document.getElementById('diagnosis').value = urlParams.get('diagnosis') || '';
    document.getElementById('prescriptions').value = urlParams.get('prescriptions') || '';
});

// Делаем строки таблицы кликабельными
document.addEventListener("DOMContentLoaded", function() {
    const clickableRows = document.querySelectorAll("#visit-list-body tr.clickable-row");
    clickableRows.forEach(function(row) {
        row.addEventListener("click", function() {
            const href = this.dataset.href;
            if (href) {
                window.location = href;
            }
        });
        row.addEventListener("mouseover", function() {
            this.classList.add("hover");
        });
        row.addEventListener("mouseout", function() {
            this.classList.remove("hover");
        });
    });
});
