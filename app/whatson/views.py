import logging
from urllib.parse import urlencode

from django.conf import settings
from django.db.models import Prefetch
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Event, Venue
from .serializers import VenueSerializer


@api_view(["GET"])
def venues(*args, **kwargs):
    two_hours_ago = timezone.now() - timezone.timedelta(hours=2)
    future_events = Event.objects.filter(starts_at__gte=two_hours_ago)
    venues = (
        Venue.objects.filter(events__in=future_events)
        .prefetch_related(Prefetch("events", queryset=future_events))
        .distinct()
    )
    serializer = VenueSerializer(venues, many=True)
    return Response(serializer.data)
