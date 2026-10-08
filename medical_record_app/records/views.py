from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import MedicalRecordForm
from .models import MedicalRecord, MedicalRecordDiagnosis


def index(request: HttpRequest) -> HttpResponse:
    """Render the index page for medical records.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered index page.
    """

    medical_records = MedicalRecord.objects.all()
    return render(request, "records/index.html", {"medical_records": medical_records})


def detail(request: HttpRequest, medical_record_id: int) -> HttpResponse:
    """Render detail page for a medical record.

    Args:
        request (HttpRequest): The HTTP request.
        medical_record_id (int): The id of the medical record derived from the URL.

    Returns:
        HttpResponse: Rendered medical record detail page.
    """
    medical_record = MedicalRecord.objects.get(pk=medical_record_id)
    return render(request, "records/detail.html", {"medical_record": medical_record})


def medical_record_create(request: HttpRequest) -> HttpResponse:
    """Render form to create a new medical record.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Form to create a new medical record.
    """
    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save()

            for diagnosis in form.cleaned_data["diagnoses"]:
                MedicalRecordDiagnosis.objects.create(
                    medical_record=record,
                    diagnosis=diagnosis,
                )
            return redirect("records:index")
    else:
        form = MedicalRecordForm()

    return render(request, "records/medical_record_form.html", {"form": form})
