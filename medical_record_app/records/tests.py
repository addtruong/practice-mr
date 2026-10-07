from datetime import timedelta 

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import Diagnosis, Resident, MedicalRecord, MedicalRecordDiagnosis

class MedicalRecordTest(TestCase):
    def setUp(self):
        Resident.objects.create(first_name="Hans", last_name="Maulwurf")
        
    def test_resident_can_only_have_one_medical_record(self):
        resident = Resident.objects.get(pk=1)
        MedicalRecord.objects.create(resident=resident)
        
        with self.assertRaises(IntegrityError):
            MedicalRecord.objects.create(resident=resident)


class MedicalRecordDiagnosisTest(TestCase):
    def setUp(self):
        Resident.objects.create(first_name="Hans", last_name="Maulwurf")
        Diagnosis.objects.create(name="Flu", description="Running nose.")
        Diagnosis.objects.create(name="Corona", description="Highly infectious.")

    def test_medical_record_can_have_same_diagnosis_twice(self):
        resident = Resident.objects.get(pk=1)
        record = MedicalRecord.objects.create(resident=resident)
        flu = Diagnosis.objects.get(name="Flu")
        corona = Diagnosis.objects.get(name="Corona")

        MedicalRecordDiagnosis.objects.create(
            medical_record=record,
            diagnosis=flu, 
            diagnosis_date=timezone.now() - timedelta(hours=2)
        )

        MedicalRecordDiagnosis.objects.create(
            medical_record=record,
            diagnosis=flu, 
            diagnosis_date=timezone.now() - timedelta(hours=1)
        )

        self.assertEqual(MedicalRecordDiagnosis.objects.count(), 2)