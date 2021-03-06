# Generated by Django 3.2.11 on 2022-02-04 03:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=3)),
                ('picture', models.ImageField(upload_to='channel_pictures')),
                ('parent_channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='channels.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)])),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channels.channel')),
            ],
        ),
        migrations.CreateModel(
            name='Pdf',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='channels.content')),
                ('author', models.CharField(max_length=50)),
                ('file', models.FileField(blank=True, null=True, upload_to='content_files/pdfs', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
            ],
            bases=('channels.content',),
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='channels.content')),
                ('genre', models.CharField(max_length=50)),
                ('file', models.FileField(blank=True, null=True, upload_to='content_files/txts', validators=[django.core.validators.FileExtensionValidator(['txt'])])),
            ],
            bases=('channels.content',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='channels.content')),
                ('movie_director', models.CharField(max_length=50)),
                ('file', models.FileField(blank=True, null=True, upload_to='content_files/videos', validators=[django.core.validators.FileExtensionValidator(['mp4'])])),
            ],
            bases=('channels.content',),
        ),
    ]
