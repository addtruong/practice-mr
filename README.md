# Medical records practice app

This project is a small application to practice Django and Bootstrap. The app represents a medical record for patients.

# Model architecture

Resident
- id
- first_name
- last_name

MedicalRecord
- id
- description
- created_at
- resident_id(FK)

Diagnosis
- id
- description

MedicalRecordDiagnosis
- id
- created_at
- diagnosis_id (FK)
- medical_record_id(FK)

Diagnostic
- id
- description

MedicalRecordDiagnostic
- id 
- description
- date
- diagnostic_id (FK)
- medical_record_id(FK)

Allergy
- id
- name 

MedicalRecordAllergy
- id 
- allergy_id(FK)
- medical_record_id(FK)

Medicine
- id 
- name

MedicalRecordMedicine
- id
- medicine_id(FK)
- medical_record_id(FK)

Operation
- id
- name 

MedicalRecordOperation
- id 
- operation_id(FK)
- medical_record_id(FK)

Isolation
- id
- status
- begin
- end
- diagnosis_id (FK)

MedicalRecordIsolation
- id 
- isolation_id(FK)
- medical_record_id(FK)