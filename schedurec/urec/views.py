from django.shortcuts import render, redirect, get_object_or_404
from .models import Class, SavedClass
from django.contrib.auth.decorators import login_required

def class_list(request):
    classes = Class.objects.all()
    return render(request, "urec/class_list.html", {"classes": classes})

@login_required
def save_class(request, class_id):
    urec_class = get_object_or_404(Class, id=class_id)
    SavedClass.objects.get_or_create(user=request.user, urec_class=urec_class)
    return redirect("urec:class_list")

@login_required
def saved_classes(request):
    saved_classes = SavedClass.objects.filter(user=request.user)
    return render(request, "urec/your_classes.html", {"saved_classes": saved_classes})

@login_required
def remove_class(request, class_id):
    SavedClass.objects.filter(user=request.user, urec_class_id=class_id).delete()
    return redirect("urec:your_classes")


import datetime
from django.http import HttpResponse
from icalendar import Calendar, Event

@login_required
def download_ics(request, class_id):
    saved = get_object_or_404(SavedClass, user=request.user, urec_class_id=class_id)
    cls = saved.urec_class

    # Parse time strings like "2:30 PM - 3:15 PM"
    start_str, end_str = cls.time.split(" - ")
    class_date = cls.date
    start_time = datetime.datetime.strptime(start_str, "%I:%M %p").time()
    end_time = datetime.datetime.strptime(end_str, "%I:%M %p").time()

    start_dt = datetime.datetime.combine(class_date, start_time)
    end_dt = datetime.datetime.combine(class_date, end_time)
    reminder_dt = start_dt - datetime.timedelta(hours=48)

    cal = Calendar()
    event = Event()
    event.add("summary", cls.name)
    event.add("dtstart", start_dt)
    event.add("dtend", end_dt)
    event.add("dtstamp", datetime.datetime.now())
    event.add("location", cls.location)
    event.add("description", "UREC Class - set by Django app")

    # Add 48-hour reminder (alarm)
    event.add('BEGIN', 'VALARM')
    event.add('TRIGGER', datetime.timedelta(hours=-48))
    event.add('DESCRIPTION', f"Reminder: {cls.name}")
    event.add('ACTION', 'DISPLAY')
    event.add('END', 'VALARM')

    cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response["Content-Disposition"] = f"attachment; filename={cls.name.replace(' ', '_')}.ics"
    return response
