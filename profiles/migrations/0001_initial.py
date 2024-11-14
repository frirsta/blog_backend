# Generated by Django 5.1.1 on 2024-11-14 12:04

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', cloudinary.models.CloudinaryField(blank=True, default='blog_media/profile_pictures/default.png', max_length=255, null=True, verbose_name='image')),
                ('cover_picture', cloudinary.models.CloudinaryField(blank=True, default='blog_media/cover_pictures/default.png', max_length=255, null=True, verbose_name='image')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
