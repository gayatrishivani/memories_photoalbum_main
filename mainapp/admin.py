from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Album)
admin.site.register(sub_album)
admin.site.register(Profile)
admin.site.register(Following)

