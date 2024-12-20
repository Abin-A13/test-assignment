from django.urls import path
from .views import CreateCSVdataView

urlpatterns = [
    path('upload_data/', CreateCSVdataView.as_view(), name="csv-upload"),
]
