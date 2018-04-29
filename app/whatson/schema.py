"""
Schema for GraphQL endpoint
"""
from graphene_django import DjangoObjectType
import graphene

from .models import Venue as VenueModel


class Venue(DjangoObjectType):
    class Meta:
        model = VenueModel


class Query(graphene.ObjectType):
    venues = graphene.List(Venue)

    def resolve_venues(self, info):
        return VenueModel.objects.all()


schema = graphene.Schema(query=Query)
