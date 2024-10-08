from django.urls import path
from .views import indexPageView, ownerPageView, propertyPageView, testPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('test/<uuid:person_uuid>/<str:owner_name>/<str:property_name>/', testPageView, name = "test"),
    path('<uuid:person_uuid>/', ownerPageView, name='owner'),
    path('<uuid:person_uuid>/<str:owner_name>/<str:property_name>/', propertyPageView, name='property'),    
]