from django.urls import path

from . import views

app_name = "records"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:medical_record_id>/", views.detail, name="detail"),
    path("<int:medical_record_id>/update", views.update, name="update"),
    path("<int:medical_record_id>/delete/", views.delete, name="delete"),
    path("new/", views.create, name="create"),
]
