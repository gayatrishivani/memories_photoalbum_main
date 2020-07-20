from django.urls import path, re_path
from .views import *



urlpatterns = [
    path('', index,name='home'),
    path('single/<int:pk>/<str:title>', single, name='single'),
    path('search/', search, name='search'),
    path('add_album/', add_album, name='add_album'),
    path('add_sub_album/<int:album_id>',add_sub_album, name='add_sub_album'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    path('<str:username>',others_profile, name='others_profile'),
    path('following/<int:id>',follow, name='following'),

]
