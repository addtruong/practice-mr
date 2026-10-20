from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    DiagnosisCreateFormSet,
    DiagnosisUpdateFormSet,
    MedicalRecordForm,
    ResidentForm,
)
from .models import MedicalRecord, MedicalRecordDiagnosis, Resident


# CRUD for medical records
def create(request: HttpRequest) -> HttpResponse:
    """Render the form to create a medical record.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Create page.
    """
    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        formset = DiagnosisCreateFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            medical_record = form.save()
            formset.instance = medical_record
            formset.save()
            return redirect("records:detail", medical_record_id=medical_record.pk)
    else:
        form = MedicalRecordForm()
        formset = DiagnosisCreateFormSet()

    context = {"form": form, "formset": formset}

    return render(
        request,
        "records/create.html",
        context,
    )


def index(request: HttpRequest) -> HttpResponse:
    """Render the index page for medical records.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered index page.
    """
    medical_records = MedicalRecord.objects.annotate(
        diagnosis_count=Count("medicalrecorddiagnosis")
    )
    context = {"medical_records": medical_records}
    return render(request, "records/index.html", context)


def detail(request: HttpRequest, medical_record_id: int) -> HttpResponse:
    """Render detail page for a medical record.

    Args:
        request (HttpRequest): The HTTP request.
        medical_record_id (int): The id of the medical record derived from the URL.

    Returns:
        HttpResponse: Rendered medical record detail page.
    """
    medical_record = get_object_or_404(MedicalRecord, id=medical_record_id)
    medical_record_diagnoses = MedicalRecordDiagnosis.objects.filter(
        medical_record=medical_record
    )
    context = {
        "medical_record": medical_record,
        "medical_record_diagnoses": medical_record_diagnoses,
    }
    return render(request, "records/detail.html", context)


def update(request: HttpRequest, medical_record_id: int) -> HttpResponse:
    """Update a medical record.

    Args:
        request (HttpRequest): The HTTP request.
        medical_record_id (int): The id of the medical record which will be updated.

    Returns:
        HttpResponse: If POST the user will be redirected, if GET the pre-populated form is shown.
    """
    medical_record = get_object_or_404(MedicalRecord, id=medical_record_id)

    if request.method == "POST":
        form = MedicalRecordForm(request.POST, instance=medical_record)
        formset = DiagnosisCreateFormSet(request.POST, instance=medical_record)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("records:detail", medical_record_id=medical_record.pk)
    else:
        form = MedicalRecordForm(instance=medical_record)
        formset = DiagnosisUpdateFormSet(instance=medical_record)

    context = {
        "form": form,
        "formset": formset,
        "medical_record": medical_record,
    }

    return render(
        request,
        "records/update.html",
        context,
    )


def delete(request: HttpRequest, medical_record_id: int) -> HttpResponse:
    """Delete an existing medical record.

    Args:
        request (HttpRequest): The Http request.
        medical_record_id (int): Id of medical record.

    Returns:
        HttpResponse: Redirect to the medical records index page.
    """
    medical_record = get_object_or_404(MedicalRecord, id=medical_record_id)

    if request.method == "POST":
        medical_record.delete()
        return redirect("records:index")

    return redirect("records:detail", medical_record_id=medical_record_id)


# Crud for residents
def resident_create(request: HttpRequest) -> HttpResponse:
    """Create view to create a resident or show a form to create a resident.

    Args:
        request (HttpRequest): The HTTP request

    Returns:
        HttpResponse: If POST save the resident to the database, else if GET show create form.
    """
    if request.method == "POST":
        form = ResidentForm(request.POST)

        if form.is_valid():
            resident = form.save()

            return redirect("records:resident_detail", resident_id=resident.id)

    else:
        form = ResidentForm()

    context = {
        "form": form,
        "title": "Create a resident",
        "button_submit": "Create a resident",
    }

    return render(request, "residents/resident_form.html", context)


def resident_index(request: HttpRequest) -> HttpResponse:
    """Render the page for all residents.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Render the page for all residents.
    """
    residents = Resident.objects.all()
    context = {"residents": residents}
    return render(request, "residents/index.html", context)


def resident_detail(request: HttpRequest, resident_id: int) -> HttpResponse:
    """View function to get the detail page a specific resident.

    Args:
        request (HttpRequest): The HTTP request
        resident_id (int): The id of the resident derived from the URL.

    Returns:
        HttpResponse: Render the detail page for resident with resident_id.
    """
    resident = get_object_or_404(Resident, pk=resident_id)
    context = {"resident": resident}
    return render(request, "residents/detail.html", context)


def resident_update(request: HttpRequest, resident_id: int) -> HttpResponse:
    """View function to update a resident.

    Args:
        request (HttpRequest): The HTTP request.
        resident_id (int): The id of the resident which should be updated.

    Returns:
        HttpResponse: Showing the update form.
    """
    resident = get_object_or_404(Resident, pk=resident_id)

    if request.method == "POST":
        form = ResidentForm(request.POST, instance=resident)

        if form.is_valid():
            form.save()
            return redirect("records:resident_detail", resident_id=resident.id)

    else:
        form = ResidentForm(instance=resident)

    context = {
        "form": form,
        "title": "Update resident",
        "button_submit": "Update resident",
    }

    return render(request, "residents/resident_form.html", context)


def resident_delete(request: HttpRequest, resident_id: int) -> HttpResponse:
    """Delete an existing resident.

    Args:
        request (HttpRequest): The HTTP request.
        resident_id (int): Id of the resident.

    Returns:
        HttpResponse: Redirect to the resident index page.
    """
    resident = get_object_or_404(Resident, pk=resident_id)

    if request.method == "POST":
        resident.delete()
        return redirect("records:resident_index")

    return redirect("records:resident_detail", resident_id=resident_id)
