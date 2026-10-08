from datetime import timedelta

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import Diagnosis, MedicalRecord, MedicalRecordDiagnosis, Resident


class MedicalRecordTest(TestCase):
    """Test the medical records for a resident."""

    def setUp(self) -> None:
        """Create a resident for test cases."""
        Resident.objects.create(first_name="Hans", last_name="Maulwurf")

    def test_resident_can_only_have_one_medical_record(self) -> None:
        """A resident can only have one medical record."""
        resident = Resident.objects.get(pk=1)
        MedicalRecord.objects.create(resident=resident)

        with self.assertRaises(IntegrityError):
            MedicalRecord.objects.create(resident=resident)


class MedicalRecordDiagnosisTest(TestCase):
    """Test class for testing the relationship between medical records and diagnosis."""

    def setUp(self) -> None:
        """Set up resident and diagnoses."""
        Resident.objects.create(first_name="Hans", last_name="Maulwurf")
        Diagnosis.objects.create(name="Flu", description="Running nose.")
        Diagnosis.objects.create(name="Corona", description="Highly infectious.")

    def test_medical_record_can_have_same_diagnosis_twice(self) -> None:
        """A medical record can have the same diagnosis several times. Only the date differs."""
        resident = Resident.objects.get(pk=1)
        record = MedicalRecord.objects.create(resident=resident)
        flu = Diagnosis.objects.get(name="Flu")

        MedicalRecordDiagnosis.objects.create(
            medical_record=record,
            diagnosis=flu,
            diagnosis_date=timezone.now() - timedelta(hours=2),
        )

        MedicalRecordDiagnosis.objects.create(
            medical_record=record,
            diagnosis=flu,
            diagnosis_date=timezone.now() - timedelta(hours=1),
        )

        self.assertEqual(MedicalRecordDiagnosis.objects.count(), 2)
