import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from icalendar import Calendar, Event
from .models import Class, SavedClass

# Helper function to group classes by weekday
def group_classes_by_weekday(classes):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    grouped = {day: [] for day in weekdays}
    for cls in classes:
        weekday_name = cls.date.strftime("%A")
        grouped[weekday_name].append(cls)
    return grouped


# 🏠 Homepage: Show all available classes organized by weekday
def class_list(request):
    selected_day = request.GET.get("day")
    all_classes = Class.objects.all()

    if selected_day:
        all_classes = all_classes.filter(date__week_day=(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(selected_day) + 2))

    # Group by weekday name
    grouped = {}
    for c in all_classes:
        weekday = c.date.strftime("%A")
        grouped.setdefault(weekday, []).append(c)

    context = {
        "grouped_classes": grouped,
        "selected_day": selected_day,
        "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    }
    return render(request, "urec/class_list.html", context)



# ➕ Save a class to "My Classes"
@login_required
def save_class(request, class_id):
    urec_class = get_object_or_404(Class, id=class_id)
    SavedClass.objects.get_or_create(user=request.user, urec_class=urec_class)
    return redirect("urec:class_list")


# ❌ Remove class from "My Classes"
@login_required
def remove_class(request, class_id):
    SavedClass.objects.filter(user=request.user, urec_class_id=class_id).delete()
    return redirect("urec:your_classes")


# 📂 View all saved classes
@login_required
def saved_classes(request):
    saved_classes = SavedClass.objects.filter(user=request.user).order_by("urec_class__date", "urec_class__time")
    return render(request, "urec/your_classes.html", {"saved_classes": saved_classes})


# 📥 Download .ics calendar file for a saved class
@login_required
def download_ics(request, class_id):
    saved = get_object_or_404(SavedClass, user=request.user, urec_class_id=class_id)
    cls = saved.urec_class

    # Parse time from "2:30 PM - 3:15 PM"
    start_str, end_str = cls.time.split(" - ")
    start_time = datetime.datetime.strptime(start_str, "%I:%M %p").time()
    end_time = datetime.datetime.strptime(end_str, "%I:%M %p").time()

    start_dt = datetime.datetime.combine(cls.date, start_time)
    end_dt = datetime.datetime.combine(cls.date, end_time)

    cal = Calendar()
    event = Event()
    event.add("summary", cls.name)
    event.add("dtstart", start_dt)
    event.add("dtend", end_dt)
    event.add("dtstamp", datetime.datetime.now())
    event.add("location", cls.location)
    event.add("description", "UREC Class via SchedUREC")

    # ⏰ Add a 48-hour reminder alarm
    alarm = Event()
    alarm.add("action", "DISPLAY")
    alarm.add("description", f"Reminder: {cls.name}")
    alarm.add("trigger", datetime.timedelta(hours=-48))
    event.add_component(alarm)

    cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type="text/calendar")
    response["Content-Disposition"] = f'attachment; filename="{cls.name.replace(" ", "_")}.ics"'
    return response
