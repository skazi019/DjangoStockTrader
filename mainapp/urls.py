from django.urls import path
from .views import stockpicker, stocktracker

urlpatterns = [
        path(route='', view=stockpicker, name='stockpicker'),
        path(route='stocktracker/', view=stocktracker, name='stocktracker')
    ]
