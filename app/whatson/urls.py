from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # FIXME: https://github.com/graphql-python/graphene-django/issues/61
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('googlee13aedb0c65b7f13.html', TemplateView.as_view(template_name='google_confirm.html')),
    path('', views.HomeView.as_view(), name='home'),
]
