from django.db import models

from user.models import User
from .list import ListField as ListField
# Create your models here.

    
def profile_directory_path(instance,filename):
    return 'User_{0}/{1}'.format(instance.user, filename)

class Gend(models.IntegerChoices):
    Male = 1
    Female = 2
    Other = 3
class Profile(models.Model):

    up_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=600, null=True,blank=True)
    profile_img = models.ImageField(upload_to=profile_directory_path,null=True,blank=True)
    name = models.CharField(max_length = 255,null=True,blank=True)
    
    gender = models.IntegerField(choices=Gend.choices,default=3)
    date_of_birth = models.DateField(null=True,blank=True)
def album_directory_path(instance, filename):
    return 'User_{0}/album_cov_{1}/{2}'.format(instance.user, instance.album_id, filename)

class Album(models.Model):
    album_id =  models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=True)
    published_date = models.DateField(auto_now_add=True)
    published_time = models.TimeField(auto_now_add=True)
    memory_date = models.DateField(null=True,blank = True)
    description = models.TextField(null=True,blank = True,max_length=300)

    Album_cover_img = models.ImageField(upload_to=album_directory_path,blank=True,null=True)
    

def user_directory_path(instance, filename):
    return 'User_{0}/{1}/{2}'.format(instance.main_title.user, instance.main_title.album_id, filename)
class sub_album(models.Model):
    id_sub =  models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    sub_title = models.CharField(max_length = 100,null=True,blank=True)
    main_title = models.ForeignKey(Album,on_delete=models.CASCADE,)
    images = models.ImageField(upload_to=user_directory_path,blank=False,null=False)
    sub_description = models.TextField(null=True,blank=True)

class Likes(models.Model):
    like_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    album_id = models.ForeignKey(Album,on_delete=models.CASCADE)
    liked_user = models.ForeignKey(User,on_delete=models.CASCADE)


class Comments(models.Model):
    album_id = models.ForeignKey(Album,on_delete=models.CASCADE)
    comment_id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    comment_text = models.TextField(null=True,blank=True)
    comment_user = models.ForeignKey(User,on_delete=models.CASCADE)

class Privacy(models.IntegerChoices):
    only_me = 1
    custom_show = 2
    custom_hide = 3

class Album_settings(models.Model):
    album_id = models.ForeignKey(Album,on_delete=models.CASCADE)
    post_notif =  models.BooleanField(default=True)
    

    private = models.IntegerField(choices=Privacy.choices)
    custom_list = ListField(null=True,blank=True)

class notifications(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pause_all = models.BooleanField(default=False)
    pause_comments = models.BooleanField(default=False)
    pause_requests = models.BooleanField(default=False)

class Account_setting(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Blocked(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_block")
    blocked_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="blocked_user")
    relation = models.BooleanField(default=True)

class Saved(models.Model):
    Saved_album = models.ForeignKey(Album,on_delete=models.CASCADE)
    user_saved = models.ForeignKey(User,on_delete=models.CASCADE)

class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    user_following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_following")
    relation = models.BooleanField(default=False)

