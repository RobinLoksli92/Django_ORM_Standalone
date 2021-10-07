import datetime

from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f"{self.owner_name} (inactive)"


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved="leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )


def get_duration(visit):
    leaved_at = visit.leaved_at if visit.leaved_at else timezone.now()
    duration_in_storage = leaved_at - visit.entered_at
    return duration_in_storage


def format_duration(duration_in_storage):
    duration_in_storage = int(duration_in_storage.total_seconds())
    duration_in_storage_hours = duration_in_storage // 3600
    duration_in_storage_minutes = (duration_in_storage % 3600) // 60
    duration_in_storage_seconds = duration_in_storage % 60
    duration_in_storage = "{} : {} : {}".format(duration_in_storage_hours,
                                                duration_in_storage_minutes,
                                                duration_in_storage_seconds
                                                )
    return duration_in_storage


def is_visit_long(visit, minutes):
    return get_duration(visit).total_seconds() > minutes * 60
