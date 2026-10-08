from django.contrib import admin

from .models import Diagnosis, MedicalRecord, MedicalRecordDiagnosis, Resident

admin.site.register(Resident)
admin.site.register(MedicalRecord)
admin.site.register(Diagnosis)
admin.site.register(MedicalRecordDiagnosis)
