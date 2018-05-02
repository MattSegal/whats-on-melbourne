"""
Schema for GraphQL endpoint
"""
from graphene_django import DjangoObjectType
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
    events = graphene.List(EventType)

    def resolve_venues(self, info):
        return Venue.objects.all()

    def resolve_events(self, info):
        return Event.objects.all()


schema = graphene.Schema(query=Query)
