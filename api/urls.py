from django.urls import path
from .views import CreateCSVdataView, request_endpoint

urlpatterns = [
    path('upload_data/', CreateCSVdataView.as_view(), name="csv-upload"),
    path('request_endpoint/', request_endpoint, name="request_endpoint"),
]
