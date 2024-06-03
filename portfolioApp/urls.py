from django.urls import path
from .views import indexPageView, analystPageView, dunkerPageView, sideprojectPageView, threeDPageView, loginPageView, characterView, translationPageView, oceanCleanupPageView, get_link_token, exchange_public_token, get_balances

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
    path('get_link_token/', get_link_token, name='get_link_token'),
    path('exchange_public_token/', exchange_public_token, name='exchange_public_token'),
    path('balances/', get_balances, name='get_balances')

]