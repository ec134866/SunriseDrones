from django.urls import path
from .views import indexPageView, analystPageView, dunkerPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('analyst/', analystPageView, name = "analyst"),
    path('dunker/', dunkerPageView, name = "dunker"),
]