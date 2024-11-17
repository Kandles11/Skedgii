from django.urls import path
from .views import JSONEndpointView

urlpatterns = [
    path('json-endpoint/', JSONEndpointView.as_view(), name='json_endpoint'),
]
