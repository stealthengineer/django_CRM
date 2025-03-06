# dcrm/urls.py
from django.urls import path
from . import views
from dcrm.views import register

urlpatterns = [
    path('', views.home, name='home'),  # This routes to the home view
]
urlpatterns = [
    path('register/', register, name='register'),  # Ensure this is defined
]
