from django.urls import path

from . import views

app_name = "records"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:medical_record_id>/", views.detail, name="detail"),
    path("new/", views.medical_record_create, name="create")
]