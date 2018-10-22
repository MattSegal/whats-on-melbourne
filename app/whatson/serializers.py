from rest_framework import serializers

from .models import Venue, Event


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = (
            'name',
            'slug',
            'address',
            'latitude',
            'longitude',
            'website',
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'name',
            'slug',
            'starts_at',
            'artist',
            'price',
            'venue',
            'event_type',
            'details_url',
            'show_search',
        )
