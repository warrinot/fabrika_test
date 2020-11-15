# Generated by Django 2.2.10 on 2020-11-15 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20201115_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('choice', models.ManyToManyField(blank=True, to='polls.Choice')),
            ],
        ),
    ]
