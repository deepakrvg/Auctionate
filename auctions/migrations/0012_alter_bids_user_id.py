# Generated by Django 3.2.7 on 2021-11-09 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_winbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='user_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
