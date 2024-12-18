from django.urls import path
from .views import indexPageView, ownerPageView, propertyPageView, testPageView, feedbackPageView, managementPageView

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('test/', testPageView, name = "test"),
    path('feedback/', feedbackPageView, name = "feedback"),
    path('management/<uuid:person_uuid>/', managementPageView, name = "management"),
    path('<uuid:person_uuid>/', ownerPageView, name='owner'),
    path('<uuid:person_uuid>/<str:owner_url_name>/<str:property_url_name>/', propertyPageView, name='property'),    
]