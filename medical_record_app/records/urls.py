from django.urls import path

from . import views

app_name = "records"

urlpatterns = [
    # Medical records
    path("", views.index, name="index"),
    path("<int:medical_record_id>/", views.detail, name="detail"),
    path("<int:medical_record_id>/update/", views.update, name="update"),
    path("<int:medical_record_id>/delete/", views.delete, name="delete"),
    path("new/", views.create, name="create"),
    # Residents
    path("residents/new", views.resident_create, name="resident_create"),
    path("residents/", views.resident_index, name="resident_index"),
    path("residents/<int:resident_id>/", views.resident_detail, name="resident_detail"),
    path(
        "residents/<int:resident_id>/update/",
        views.resident_update,
        name="resident_update",
    ),
    path(
        "residents/<int:resident_id>/delete/",
        views.resident_delete,
        name="resident_delete",
    ),
]
