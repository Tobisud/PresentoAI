# Generated by Django 5.1.1 on 2024-10-17 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='presento',
            name='process_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='presento',
            name='voice_model',
            field=models.IntegerField(default=1),
        ),
    ]
