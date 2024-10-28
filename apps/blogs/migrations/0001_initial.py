# Generated by Django 5.0.7 on 2024-10-26 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('users', '0002_follow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=512)),
                ('owner',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts',
                                   to='users.profile')),
            ],
            options={
                'unique_together': {('owner', 'slug')},
            },
        ),
    ]