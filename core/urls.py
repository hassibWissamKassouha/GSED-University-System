from django import views
from django.urls import path
from .views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', views.get_user_profile, name='user-profile'),
]