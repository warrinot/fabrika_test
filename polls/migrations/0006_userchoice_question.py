# Generated by Django 2.2.10 on 2020-11-15 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20201115_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchoice',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_choices', to='polls.Question'),
            preserve_default=False,
        ),
    ]