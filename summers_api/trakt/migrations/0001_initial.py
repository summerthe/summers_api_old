# Generated by Django 3.2.10 on 2022-01-03 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('thumbnail', models.ImageField(upload_to='thumbnails')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='guid')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('categories', models.ManyToManyField(blank=True, to='trakt.Category')),
            ],
            options={
                'verbose_name': 'Show',
                'verbose_name_plural': 'Shows',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='UsersShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('watched_episode', models.PositiveSmallIntegerField(default=0)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersshow', to='trakt.show')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersshow', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': "User's show",
                'verbose_name_plural': "User's shows",
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('season', models.PositiveIntegerField(default=1)),
                ('episode', models.PositiveIntegerField(default=8)),
                ('show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trakt.show')),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
                'ordering': ['-show__updated_at', 'season'],
            },
        ),
    ]
