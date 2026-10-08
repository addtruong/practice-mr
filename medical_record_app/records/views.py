from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DiagnosisCreateFormSet, DiagnosisUpdateFormSet, MedicalRecordForm
from .models import MedicalRecord, Resident


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


def create(request: HttpRequest) -> HttpResponse:
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

    return render(request, "records/create.html", {"form": form, "formset": formset})


def update(request: HttpRequest, medical_record_id: int) -> HttpResponse:
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

    return render(
        request,
        "records/update.html",
        {
            "form": form,
            "formset": formset,
            "medical_record": medical_record,
        },
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


# def create(request: HttpRequest) -> HttpResponse:
#     """Render form to create a new medical record.

#     Args:
#         request (HttpRequest): The HTTP request.

#     Returns:
#         HttpResponse: Form to create a new medical record.
#     """
#     residents_without_medical_record = Resident.objects.filter(
#         medicalrecord__isnull=True
#     )

#     if request.method == "POST":
#         resident_id = request.POST["resident"]
#         resident = get_object_or_404(Resident, pk=resident_id)

#         if MedicalRecord.objects.filter(resident=resident).exists():
#             return render(
#                 request,
#                 "records/create.html",
#                 {
#                     "residents": residents_without_medical_record,
#                     "error": "This resident already has medical record.",
#                 },
#                 status=400,
#             )

#         medical_record = MedicalRecord.objects.create(resident=resident)
#         return redirect("records:detail", medical_record_id=medical_record.pk)

#     return render(
#         request, "records/create.html", {"residents": residents_without_medical_record}
#     )


# def update(request: HttpRequest, medical_record_id: int) -> HttpResponse:
#     """Render update page to update an existing medical record.

#     Args:
#         request (HttpRequest): The HTTP request.
#         medical_record_id (int): ID of medical record.

#     Returns:
#         HttpResponse: Form to update an existing medical record.
#     """
#     medical_record = get_object_or_404(MedicalRecord, id=medical_record_id)

#     if request.method == "POST":
#         resident_id = request.POST["resident"]
#         resident = get_object_or_404(Resident, pk=resident_id)
#         medical_record.resident = resident
#         medical_record.save()

#         return redirect("records:detail", medical_record_id=medical_record.pk)

#     residents = Resident.objects.filter(
#         Q(medicalrecord__isnull=True) | Q(pk=medical_record.resident_id)
#     )

#     return render(
#         request,
#         "records/update.html",
#         {
#             "medical_record": medical_record,
#             "residents": residents,
#         },
#     )
