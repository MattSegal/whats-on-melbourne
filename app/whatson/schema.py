"""
Schema for GraphQL endpoint
"""
from django.db.models import Prefetch
from django.utils import timezone
from graphene_django import DjangoObjectType, DjangoConnectionField
import graphene

from .models import Venue, Event


class VenueType(DjangoObjectType):
    class Meta:
        model = Venue


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class Query(graphene.ObjectType):
    venues = graphene.List(VenueType)

    def resolve_venues(self, info):
        """
        Returns all venues with events today, also filter events by date
        """
        now = timezone.localtime()
        today_naieve = timezone.datetime(year=now.year, month=now.month, day=now.day)
        today = timezone.make_aware(today_naieve)
        event_prefetch = Prefetch(
           'events',
           queryset=Event.objects.filter(starts_at__gte=today).order_by('starts_at')
        )
        return (
            Venue.objects
            .prefetch_related(event_prefetch)
            .filter(events__starts_at__gte=today)
            .all()
        )


schema = graphene.Schema(query=Query)
