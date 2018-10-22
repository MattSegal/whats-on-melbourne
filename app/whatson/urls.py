from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'event', views.EventViewSet, 'event')
router.register(r'venue', views.VenueViewSet, 'venue')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', views.HomeView.as_view(), name='home'),
]
