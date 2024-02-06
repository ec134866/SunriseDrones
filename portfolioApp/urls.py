from django.urls import path
from .views import indexPageView, analystPageView, dunkerPageView, sideprojectPageView, threeDPageView, loginPageView, characterView, translationPageView, oceanCleanupPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('analyst/', analystPageView, name = "analyst"),
    path('dunker/', dunkerPageView, name = "dunker"),
    path('sideprojects/', sideprojectPageView, name = "sideprojects"),
    path('sideprojects/3D/', threeDPageView, name = "threeD"),
    path('sideprojects/translation/', translationPageView, name = "translation"),
    path('theOceanCleanup/', oceanCleanupPageView, name = "oceanCleanup"),
    path('login/', loginPageView, name='login'),
    path('mascot/', characterView, name='character'),

]