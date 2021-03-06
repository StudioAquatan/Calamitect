# Generated by Django 2.1.3 on 2018-11-04 05:12

import boards.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('category_type', models.IntegerField(default=0, verbose_name='category')),
                ('image', models.ImageField(upload_to=boards.models.get_image_path, verbose_name='image')),
                ('draft_flag', models.BooleanField(verbose_name='draft-flag')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='text')),
                ('image', models.ImageField(upload_to=boards.models.get_image_path, verbose_name='image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='boards.Article', verbose_name='article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='boards.Article', verbose_name='article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date_created')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.Article', verbose_name='article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='tag')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.Article', verbose_name='article')),
            ],
        ),
    ]
