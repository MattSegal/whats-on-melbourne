from rest_framework import serializers

from .models import Event, Venue


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "slug",
            "starts_at",
            "artist",
            "price",
            "event_type",
            "details_url",
            "show_search",
        )


class VenueSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)

    class Meta:
        model = Venue
        fields = (
            "id",
            "name",
            "events",
            "slug",
            "address",
            "latitude",
            "longitude",
            "website",
        )
