from django.urls import path
from .views import indexPageView,  sideprojectPageView, loginPageView, sunrisePageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('sideprojects/', sideprojectPageView, name = "sideprojects"),
    path('login/', loginPageView, name='login'),
    path('sunrise/', sunrisePageView, name='sunrise-model')

]