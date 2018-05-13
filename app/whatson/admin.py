from django.contrib import admin
from django.contrib.messages import constants as messages

from .models import Venue, Event, Source
from .tasks import geocode_venue


admin.site.register(Source)

@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ['name', 'venue', 'starts_at']
    list_filter = ['starts_at', 'venue']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    actions = ['geoencode']

    def geoencode(self, request, queryset):
        for venue in queryset:
            is_not_encoded = not (
                venue.address and
                venue.latitude and
                venue.longitude
            )
            if is_not_encoded:
                geocode_venue.delay(venue.pk)

        self.message_user(request, 'Geoencoding tasks dispatched.', level=messages.INFO)

    geoencode.short_description = 'Geoencode venues'

