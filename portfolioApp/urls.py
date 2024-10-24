from django.urls import path
from .views import indexPageView, ownerPageView, propertyPageView, testPageView, feedbackPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('test/', testPageView, name = "test"),
    path('feedback/', feedbackPageView, name = "feedback"),
    path('<uuid:person_uuid>/', ownerPageView, name='owner'),
    path('<uuid:person_uuid>/<str:owner_name>/<str:property_name>/', propertyPageView, name='property'),    
]