# Generated by Django 2.2.10 on 2020-11-15 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_userchoice_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchoice',
            name='text_choice',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]