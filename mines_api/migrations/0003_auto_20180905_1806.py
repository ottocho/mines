# Generated by Django 2.1 on 2018-09-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mines_api', '0002_auto_20180905_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='is_finished',
        ),
        migrations.AddField(
            model_name='game',
            name='status',
            field=models.IntegerField(choices=[(10, 'playing game'), (20, 'game won'), (30, 'game lost')], default=10),
        ),
    ]
