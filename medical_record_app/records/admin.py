from django.contrib import admin
from .models import Resident, MedicalRecord, Diagnosis, MedicalRecordDiagnosis

admin.site.register(Resident)
admin.site.register(MedicalRecord)
admin.site.register(Diagnosis)
admin.site.register(MedicalRecordDiagnosis)