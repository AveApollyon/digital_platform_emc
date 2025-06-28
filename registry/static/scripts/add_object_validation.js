// add_object_validation.js

document.addEventListener('DOMContentLoaded', function() {
    var form = document.querySelector('.input-row');

    form.addEventListener('input', function(event) {
        var target = event.target;
        if (!target.matches('input')) return;

        validateField(target);
    });
});

function validateField(input) {
    var fieldName = input.getAttribute('name');
    var value = input.value;

    var form = input.closest('form');
    var fieldValidators = form.getAttribute('data-field-validators');
    if (!fieldValidators) return;

    var validators = JSON.parse(fieldValidators);
    if (!validators[fieldName]) return;

    var errors = [];
    validators[fieldName].forEach(function(validator) {
        var error = validator(value);
        if (error) {
            errors.push(error);
        }
    });

    updateFieldValidation(input, errors.length > 0);
}

function updateFieldValidation(input, isValid) {
    if (isValid) {
        input.classList.remove('is-invalid');
    } else {
        input.classList.add('is-invalid');
    }
}
