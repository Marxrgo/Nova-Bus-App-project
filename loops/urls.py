from django.urls import path
from . import views

app_name = "loops"

urlpatterns = [
    path("", views.loop_index, name="index"),
    path("loop/<str:loop>/", views.loop_dashboard, name = "loop_dashboard"),
    path("slot/<int:slot_id>/update/", views.update_slot, name="update_slot"),
    path("loop/<str:loop>/clear/", views.clear_loop, name = "clear_loop")
]