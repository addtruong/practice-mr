from django.db import models

class Resident(models.Model):
    """
    Django model for a resident.
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name}"


class MedicalRecord(models.Model):
    """
    Django model for a medical record. 
    
    There is a one-to-one relationship between a medical record and a resident.
    """
    resident = models.OneToOneField(Resident, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.id} - Medical record for {self.resident}"