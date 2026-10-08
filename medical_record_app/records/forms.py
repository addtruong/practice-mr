from django import forms
from django.db.models import Q

from .models import MedicalRecord, MedicalRecordDiagnosis, Resident


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ["resident"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dein Q-Filter, jetzt an einer Stelle, die auch beim POST validiert wird
        self.fields["resident"].queryset = Resident.objects.filter(
            Q(medicalrecord__isnull=True) | Q(pk=self.instance.resident_id)
        )


class MedicalRecordDiagnosisForm(forms.ModelForm):
    class Meta:
        model = MedicalRecordDiagnosis
        fields = ["diagnosis", "diagnosis_date"]  # noqa: RUF012
        widgets = {  # noqa: RUF012
            "diagnosis_date": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
        }


DiagnosisFormSet = forms.inlineformset_factory(
    MedicalRecord,
    MedicalRecordDiagnosis,
    form=MedicalRecordDiagnosisForm,
    extra=1,
    can_delete=True,
)
