from django import forms

from .models import Diagnosis, MedicalRecord, Resident


class MedicalRecordForm(forms.ModelForm):
    """Provide a form for creating and editing medical records."""

    diagnoses = forms.ModelMultipleChoiceField(
        queryset=Diagnosis.objects.all(),
        required=False,
    )

    class Meta:
        model = MedicalRecord
        fields = ["resident"]  # noqa: RUF012

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["resident"].queryset = Resident.objects.filter(
            medicalrecord__isnull=True
        )
