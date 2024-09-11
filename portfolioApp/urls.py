from django.urls import path
from .views import indexPageView,  sideprojectPageView, loginPageView, sunrisePageView, ownerPageView, propertyPageView, threeDexteriorPageView, threeDinteriorPageView, overflightPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('<uuid:person_uuid>/', ownerPageView, name='owner'),
    path('<uuid:person_uuid>/<str:property_name>/', propertyPageView, name='property'),

    # rid of the following not necessary
    path('sideprojects/', sideprojectPageView, name = "sideprojects"),
    path('login/', loginPageView, name='login'),
    path('sunrise/', sunrisePageView, name='sunrise-model'),

    # rid of the following when property is correct
    path('overflight/', overflightPageView, name='overflight'),
    path('interior/', threeDinteriorPageView, name='interior'),
    path('exterior/', threeDexteriorPageView, name='exterior')
    
]