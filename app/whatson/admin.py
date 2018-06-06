from django.contrib import admin
from django.contrib.messages import constants as messages

from .models import Venue, Event, Source
from .tasks import geocode_venue, run_scraper


@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ['name', 'venue', 'starts_at']
    list_filter = ['starts_at', 'event_type']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    actions = ['geocode']

    def geocode(self, request, queryset):
        for venue in queryset:
            is_not_encoded = not (
                venue.address and
                venue.latitude and
                venue.longitude
            )
            if is_not_encoded:
                geocode_venue.delay(venue.pk)

        self.message_user(request, 'Geocoding tasks dispatched.', level=messages.INFO)

    geocode.short_description = 'Geocode venues'


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    actions = ['scrape']

    def scrape(self, request, queryset):
        for source in queryset:
            run_scraper.delay(source.pk)

        self.message_user(request, 'Scraping tasks dispatched.', level=messages.INFO)

    scrape.short_description = 'Scrape sources'
