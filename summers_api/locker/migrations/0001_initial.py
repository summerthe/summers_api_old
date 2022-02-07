# Generated by Django 4.0.1 on 2022-02-05 18:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='guid')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('is_pinned', models.BooleanField(blank=True, default=False)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='note/folder-icons/')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='guid')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Folder',
                'verbose_name_plural': 'Folders',
                'ordering': ['-is_pinned', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.CharField(blank=True, choices=[('SCRATCHPAD', 'SCRATCHPAD'), ('DEFAULT', 'DEFAULT'), ('FAVOURITE', 'FAVOURITE'), ('TRASH', 'TRASH')], default='DEFAULT', max_length=10)),
                ('is_pinned', models.BooleanField(blank=True, default=False)),
                ('bg_image', models.ImageField(blank=True, null=True, upload_to='note/bg-images/')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='guid')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
                'ordering': ['-is_pinned', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Vault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='note/vault-icons/')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='guid')),
                ('slug', models.SlugField(editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Vault',
                'verbose_name_plural': 'Vaults',
                'ordering': ['-created_at'],
            },
        ),
    ]
