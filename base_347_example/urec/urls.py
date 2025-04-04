from django.urls import path
from . import views

app_name = "urec"

urlpatterns = [
    path("", views.class_list, name="class_list"),  # Homepage
    path("save-class/<int:class_id>/", views.save_class, name="save_class"),
    path("your-classes/", views.saved_classes, name="your_classes"),
    path("remove-class/<int:class_id>/", views.remove_class, name="remove_class"),
    path("download-ics/<int:class_id>/", views.download_ics, name="download_ics"),


]
