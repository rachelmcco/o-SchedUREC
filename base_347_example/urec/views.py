from django.shortcuts import render
from .models import Class

def dashboard(request):
    classes = Class.objects.all()
    return render(request, "urec/dashboard.html", {"classes": classes})
