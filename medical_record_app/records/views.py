from django.shortcuts import redirect, render
from .models import MedicalRecord, MedicalRecordDiagnosis
from .forms import MedicalRecordForm

# Create your views here.
def index(request):
    medical_records = MedicalRecord.objects.all()
    return render(request, "records/index.html", {"medical_records": medical_records})

def detail(request, medical_record_id): 
    medical_record = MedicalRecord.objects.get(pk=medical_record_id)
    return render(request, "records/detail.html", {"medical_record": medical_record})

def medical_record_create(request): 
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
    
    return render(request, "records/medical_record_form.html",  {"form": form})