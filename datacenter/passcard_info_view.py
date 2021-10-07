from datacenter.models import Passcard, Visit, get_duration, format_duration, is_visit_long
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    all_visits_of_selected_passcard = Visit.objects.filter(passcard=passcard)
    selected_passcard_visits_info = []
    for visit in all_visits_of_selected_passcard:
        duration_in_storage = get_duration(visit)
        selected_passcard_visits_info.append(
            {
                "entered_at": visit.entered_at,
                "duration": format_duration(duration_in_storage),
                "is_strange": is_visit_long(visit, 60)
            },
        )
    context = {
        "passcard": passcard,
        "this_passcard_visits": selected_passcard_visits_info
    }
    return render(request, "passcard_info.html", context)
