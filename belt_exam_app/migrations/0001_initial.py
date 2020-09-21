# Generated by Django 2.2.4 on 2020-09-21 17:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=45)),
                ('last_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=255)),
                ('password', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wish_name', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=255)),
                ('granted', models.BooleanField(default=False)),
                ('likes', models.IntegerField()),
                ('date_granted', models.DateTimeField(default=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_by', models.ManyToManyField(to='belt_exam_app.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishes', to='belt_exam_app.User')),
            ],
        ),
    ]