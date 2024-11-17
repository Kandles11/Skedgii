from django.urls import path
from .views import JSONEndpointView, PuckEndpoint

urlpatterns = [
    path('json-endpoint/', JSONEndpointView.as_view(), name='json_endpoint'),
    path('puck/', PuckEndpoint.as_view(), name='json_endpoint'),
]
