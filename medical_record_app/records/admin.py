from django.contrib import admin
from .models import Resident, MedicalRecord

admin.site.register(Resident)
admin.site.register(MedicalRecord)