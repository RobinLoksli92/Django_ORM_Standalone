from datacenter.models import Passcard, Visit, get_duration, format_duration
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    all_non_closed_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in all_non_closed_visits:
        duration_in_storage = get_duration(visit)
        non_closed_visits.append({
            "who_entered": visit.passcard,
            "entered_at": timezone.localtime(value=visit.entered_at),
            "duration": format_duration(duration_in_storage)
        })
    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, "storage_information.html", context)
