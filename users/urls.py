from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('personal/', views.UserInfo.as_view(), name='user_info'),

]
