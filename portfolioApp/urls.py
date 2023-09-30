from django.urls import path
from .views import indexPageView, analystPageView, dunkerPageView, sideprojectPageView, threeDPageView, loginPageView, characterView, translationPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('analyst/', analystPageView, name = "analyst"),
    path('dunker/', dunkerPageView, name = "dunker"),
    path('sideprojects/', sideprojectPageView, name = "sideprojects"),
    path('3D/', threeDPageView, name = "threeD"),
    path('translation/', translationPageView, name = "translation"),
    path('login/', loginPageView, name='login'),
    path('character/', characterView, name='character'),

]