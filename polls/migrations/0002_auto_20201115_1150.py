# Generated by Django 2.2.10 on 2020-11-15 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='ended',
            field=models.DateTimeField(null=True),
        ),
    ]
