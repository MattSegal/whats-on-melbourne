import logging
from urllib.parse import urlencode

from django.conf import settings
from django.views.generic import TemplateView
from rest_framework import viewsets

from .serializers import EventSerializer, VenueSerializer
from .models import Event, Venue


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VenueSerializer
    queryset = Venue.objects.all()


class FrontendView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maps_js_url = 'https://maps.googleapis.com/maps/api/js'
        maps_params = {
            'v': '3.exp',
            'libraries': 'geometry,drawing,places',
        }
        if settings.GOOGLE_MAPS_JS_API_KEY:
            maps_params['key'] = settings.GOOGLE_MAPS_JS_API_KEY
        context['maps_js_url'] = '{}?{}'.format(
            maps_js_url, urlencode(maps_params)
        )

        context['description'] = 'Discover music and events that are on tonight in Melbourne'
        context['title'] = 'What\'s On Melbourne'
        context['canonical_url'] = 'https://whatsonmelb.fun'
        context['enable_analytics'] = not settings.DEBUG
        return context
