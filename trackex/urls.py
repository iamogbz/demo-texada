"""
Configure the base url endpoints for trackex.api
"""

from django.conf.urls import url, include
from rest_framework import routers
from api import views as api_views

ROUTER = routers.DefaultRouter(trailing_slash=False)
ROUTER.register(r'status', api_views.StatusViewSet)
ROUTER.register(r'packages', api_views.PackageViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(ROUTER.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
