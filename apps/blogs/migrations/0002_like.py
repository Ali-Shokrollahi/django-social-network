# Generated by Django 5.0.7 on 2024-10-31 08:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blogs', '0001_initial'),
        ('users', '0002_follow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blogs.post')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes',
                                              to='users.profile')),
            ],
            options={
                'unique_together': {('profile', 'post')},
            },
        ),
    ]