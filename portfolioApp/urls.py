from django.urls import path
from .views import indexPageView, ownerPageView, propertyPageView, testPageView, feedbackPageView, managementPageView, download_zip

urlpatterns = [
    path('', indexPageView, name = "index"),
    path('test/', testPageView, name = "test"),
    path('feedback/', feedbackPageView, name = "feedback"),
    path('management/<uuid:person_uuid>/', managementPageView, name = "management"),
	path('<uuid:person_uuid>/<str:owner_url_name>/<str:property_url_name>/', propertyPageView, name='property'),    
	path('<uuid:person_uuid>/download-zip/', download_zip, name='download_zip'),
    path('<uuid:person_uuid>/', ownerPageView, name='owner'),
]