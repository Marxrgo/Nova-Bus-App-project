from django.urls import path
from . import views

app_name = "AM"

urlpatterns = [
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/<int:status_id>/arrived/", views.mark_arrived, name="mark_arrived"),
    path("staff/<int:status_id>/delete/", views.delete_status, name="delete_status"),
    path("bus/<int:number>/", views.bus_status, name="bus_status"),
]