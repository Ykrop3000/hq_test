# Generated by Django 4.2.5 on 2023-09-21 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonviewhistory',
            name='duration',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
