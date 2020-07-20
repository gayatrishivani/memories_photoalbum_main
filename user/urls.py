from django.urls import path, re_path
from .views import *



urlpatterns = [
    path('login/',login,name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',logout,name='logout')
]