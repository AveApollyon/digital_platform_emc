from django.contrib import admin

import entities.models as models

admin.site.register(models.Patient)
admin.site.register(models.Doctor)
admin.site.register(models.Visit)
admin.site.register(models.MedicalCard)