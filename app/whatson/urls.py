from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # FIXME: https://github.com/graphql-python/graphene-django/issues/61
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('', views.HomeView.as_view(), name='home'),
]
