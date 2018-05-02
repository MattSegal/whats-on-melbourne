from django.contrib import admin
from django.contrib.messages import constants as messages

from .models import Venue, Event
from .tasks import geocode_venue


admin.site.register(Event)

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

