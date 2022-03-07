# Generated by Django 4.0.1 on 2022-03-07 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locker', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vault',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='note',
            name='categories',
            field=models.ManyToManyField(blank=True, to='locker.Category'),
        ),
        migrations.AddField(
            model_name='note',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.folder'),
        ),
        migrations.AddField(
            model_name='folder',
            name='vault',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locker.vault'),
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
