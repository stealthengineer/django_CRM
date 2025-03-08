# dcrm/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from .views import get_chat_message

urlpatterns = [
    path('', views.home, name='home'),  # This routes to the home view
    path('admin/', admin.site.urls),

    path('login/', views.login_user, name='login'),  # Changed name to 'login'
    path('logout/', views.logout_user, name='logout'),  # Changed name to 'logout'
    path('dashboard/', views.dashboard, name='dashboard'),  # New dashboard path
    path('register/', views.register, name='register'), # New register path
    path("api/chat-message/", get_chat_message, name="chat_message"),

]
