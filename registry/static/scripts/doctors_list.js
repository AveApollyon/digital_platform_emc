document.addEventListener("DOMContentLoaded", function() {
    const filterButton = document.getElementById('filter-doctors');
    filterButton.addEventListener('click', function() {
        const lastName = document.getElementById('last_name').value;
        const firstName = document.getElementById('first_name').value;
        const middleName = document.getElementById('middle_name').value;
        const dateOfBirth = document.getElementById('date_of_birth').value;
        const gender = document.getElementById('gender').value;
        const phoneNumber = document.getElementById('phone_number').value;
        const specialty = document.getElementById('specialty').value;

        const url = new URL(window.location.href);
        url.searchParams.set('last_name', lastName);
        url.searchParams.set('first_name', firstName);
        url.searchParams.set('middle_name', middleName);
        url.searchParams.set('date_of_birth', dateOfBirth);
        url.searchParams.set('gender', gender);
        url.searchParams.set('phone_number', phoneNumber);
        url.searchParams.set('specialty', specialty);

        window.location.href = url.href;
    });

    const urlParams = new URLSearchParams(window.location.search);
    document.getElementById('last_name').value = urlParams.get('last_name') || '';
    document.getElementById('first_name').value = urlParams.get('first_name') || '';
    document.getElementById('middle_name').value = urlParams.get('middle_name') || '';
    document.getElementById('date_of_birth').value = urlParams.get('date_of_birth') || '';
    document.getElementById('gender').value = urlParams.get('gender') || '';
    document.getElementById('phone_number').value = urlParams.get('phone_number') || '';
    document.getElementById('specialty').value = urlParams.get('specialty') || '';

    const doctorListBody = document.getElementById('doctor-list-body');
    doctorListBody.addEventListener('click', function(event) {
        if (event.target.tagName === 'TD' || event.target.tagName === 'TR') {
            const row = event.target.closest('tr');
            const href = row ? row.dataset.href : null;
            if (href) {
                window.location = href;
            }
        }
    });

    const clickableRows = document.querySelectorAll("#doctor-list-body tr.clickable-row");
    clickableRows.forEach(function(row) {
        row.addEventListener("mouseover", function() {
            this.classList.add("hover");
        });
        row.addEventListener("mouseout", function() {
            this.classList.remove("hover");
        });
    });
});
