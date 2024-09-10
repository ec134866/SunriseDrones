from django.urls import path
from .views import indexPageView,  sideprojectPageView, loginPageView, sunrisePageView, ownerPageView, propertyPageView, threeDexteriorPageView, threeDinteriorPageView, overflightPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('sideprojects/', sideprojectPageView, name = "sideprojects"),
    path('login/', loginPageView, name='login'),
    path('owner/', ownerPageView, name='owner'),
    path('overflight/', overflightPageView, name='overflight'),
    path('interior/', threeDinteriorPageView, name='interior'),
    path('exterior/', threeDexteriorPageView, name='exterior'),
    # change owner & property to [] variables 
    path('property/', propertyPageView, name='property'),
    path('sunrise/', sunrisePageView, name='sunrise-model')

]