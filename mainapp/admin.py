from django.contrib import admin
from .models import Album,sub_album,Profile
# Register your models here.

admin.site.register(Album)
admin.site.register(sub_album)
admin.site.register(Profile)


