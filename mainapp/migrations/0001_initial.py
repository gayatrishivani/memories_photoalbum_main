# Generated by Django 3.0.8 on 2020-07-21 19:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainapp.list
import mainapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('published_date', models.DateField(auto_now_add=True)),
                ('published_time', models.TimeField(auto_now_add=True)),
                ('memory_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('Album_cover_img', models.ImageField(blank=True, null=True, upload_to=mainapp.models.album_directory_path)),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='sub_album',
            fields=[
                ('id_sub', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('images', models.ImageField(upload_to=mainapp.models.user_directory_path)),
                ('sub_description', models.TextField(blank=True, null=True)),
                ('main_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Saved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Saved_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Album')),
                ('user_saved', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('up_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=600, null=True)),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to=mainapp.models.profile_directory_path)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=3)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pause_all', models.BooleanField()),
                ('pause_comments', models.BooleanField()),
                ('pause_requests', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('like_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Album')),
                ('liked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('user_following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(blank=True, null=True)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Album')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Blocked',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.BooleanField(default=True)),
                ('blocked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocked_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_block', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Album_settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_notif', models.BooleanField(default=True)),
                ('private', models.IntegerField(choices=[(1, 'Only Me'), (2, 'Custom Show'), (3, 'Custom Hide')])),
                ('custom_list', mainapp.list.ListField(blank=True, null=True)),
                ('album_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Album')),
            ],
        ),
        migrations.CreateModel(
            name='Account_setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
