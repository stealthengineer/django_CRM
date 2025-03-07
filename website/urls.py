# dcrm/urls.py
from django.urls import path
from . import views  # If your views are in the same "dcrm" module
                     # or from dcrm.views import (home, login_user, logout_user, register, dashboard)

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Register page
    path('register/', views.register, name='register'),

    # Login and logout (if you want them routed here too):
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboard (requires login)
    path('dashboard/', views.dashboard, name='dashboard'),
]
