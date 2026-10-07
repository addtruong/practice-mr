from django.db import IntegrityError
from django.test import TestCase

from .models import Resident, MedicalRecord

class MedicalRecordTest(TestCase):
    def setUp(self):
        Resident.objects.create(first_name="Hans", last_name="Maulwurf")
        
    def test_resident_can_only_have_one_medical_record(self):
        resident = Resident.objects.get(pk=1)
        MedicalRecord.objects.create(resident=resident)
        
        with self.assertRaises(IntegrityError):
            MedicalRecord.objects.create(resident=resident)


