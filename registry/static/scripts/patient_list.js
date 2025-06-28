const patientListBody = document.getElementById('patient-list-body');

document.addEventListener("DOMContentLoaded", function() {
    const filterButton = document.getElementById('filter-patients');
    filterButton.addEventListener('click', function() {
        const lastName = document.getElementById('last_name').value;


        const url = new URL(window.location.href);
        url.searchParams.set('last_name', lastName);
        url.searchParams.set('first_name', firstName);
        url.searchParams.set('middle_name', middleName);
        url.searchParams.set('date_of_birth', dateOfBirth);
        url.searchParams.set('gender', gender);
        url.searchParams.set('phone_number', phoneNumber);

        window.location.href = url.href;
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById('last_name').value = urlParams.get('last_name') || '';
    document.getElementById('first_name').value = urlParams.get('first_name') || '';
    document.getElementById('middle_name').value = urlParams.get('middle_name') || '';
    document.getElementById('date_of_birth').value = urlParams.get('date_of_birth') || '';
    document.getElementById('gender').value = urlParams.get('gender') || '';
    document.getElementById('phone_number').value = urlParams.get('phone_number') || '';
});


// Делаем строки таблицы кликабельными
patientListBody.addEventListener('click', (event) => {
    if (event.target.tagName === 'TR') {
        const row = event.target;
        const href = row.dataset.href;
        if (href) {
            window.location = href;
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const clickableRows = document.querySelectorAll("#patient-list-body tr.clickable-row");
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
