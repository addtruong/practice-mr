from datetime import datetime

from django import forms
from django.db.models import Q

from .models import MedicalRecord, MedicalRecordDiagnosis, Resident


# Forms for residents
class ResidentForm(forms.ModelForm):
    class Meta:
        model = Resident
        fields = "__all__"

        widgets = {  # noqa: RUF012
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }


# Forms for medical record
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["resident"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["resident"].queryset = Resident.objects.filter(
            Q(medicalrecord__isnull=True) | Q(pk=self.instance.resident_id)
        )


class MedicalRecordDiagnosisForm(forms.ModelForm):
    class Meta:
        model = MedicalRecordDiagnosis
        fields = ["diagnosis", "diagnosis_date"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "diagnosis_date": forms.DateInput(
                attrs={"type": "date", "max": datetime.now().date()}, format="%Y-%m-%d"
            ),
        }

    def clean_diagnosis_date(self):
        diagnosis_date = self.cleaned_data["diagnosis_date"]

        if diagnosis_date is not None and diagnosis_date > datetime.now().date():
            raise forms.ValidationError("Diagnosis date cannot be in the future.")

        return diagnosis_date


# A medical record has several diagnoses, therefore we need a list of forms (a FormSet)
DiagnosisUpdateFormSet = forms.inlineformset_factory(
    MedicalRecord,
    MedicalRecordDiagnosis,
    form=MedicalRecordDiagnosisForm,
    extra=1,
    can_delete=True,
)

DiagnosisCreateFormSet = forms.inlineformset_factory(
    MedicalRecord,
    MedicalRecordDiagnosis,
    form=MedicalRecordDiagnosisForm,
    extra=3,
    can_delete=False,
)
