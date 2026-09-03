from django.urls import path
from . import views

app_name = "loops"

urlpatterns = [
    path("", views.loop_dashboard, name="dashboard"),
    path("slot/<int:slot_id>/update/", views.update_slot, name="update_slot"),
]