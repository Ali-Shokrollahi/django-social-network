# Generated by Django 5.0.7 on 2024-07-28 06:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('username', models.CharField(max_length=32, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=32, null=True)),
                ('last_name', models.CharField(blank=True, max_length=32, null=True)),
                ('bio', models.CharField(blank=True, max_length=255, null=True)),
                ('post_count', models.PositiveIntegerField(default=0)),
                ('follower_count', models.PositiveIntegerField(default=0)),
                ('following_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
