# Generated by Django 2.1 on 2018-09-05 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mines_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brick',
            name='is_mine',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='brick',
            name='x',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='brick',
            name='y',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
