from django.db import models


class Resident(models.Model):
    """Represent a resident."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class MedicalRecord(models.Model):
    """Represent a medical record for a resident.

    There is a one-to-one relationship between a medical record and a resident.
    """

    resident = models.OneToOneField(
        Resident, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"Medical record for {self.resident}"


class Diagnosis(models.Model):
    """Represent a diagnosis which is associated with a medical record."""

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=300)

    # Relationships
    medical_records = models.ManyToManyField(
        MedicalRecord, through="MedicalRecordDiagnosis", related_name="diagnoses"
    )

    class Meta:
        verbose_name_plural = "Diagnoses"

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class MedicalRecordDiagnosis(models.Model):
    """
    Represent the association table for diagnoses in medical records.

    Many-to-many
        - A diagnosis can be in multiple medical records
        - A medical record can have multiple diagnosis

    Further attributes:
        - diagnosis_date
    """

    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE)
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE)
    diagnosis_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Medical record diagnoses"

    def __str__(self) -> str:
        date = (
            self.diagnosis_date("5d.%m.%Y") if self.diagnosis_date else "unknown date"
        )
        return f"{self.medical_record}: {self.diagnosis} diagnosed at {date}"
