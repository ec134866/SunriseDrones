from django.urls import path
from .views import indexPageView, analystPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('/businessanalyst', analystPageView, name = "analyst"),
]