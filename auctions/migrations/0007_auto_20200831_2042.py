# Generated by Django 3.0.3 on 2020-08-31 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200831_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='image',
            field=models.URLField(),
        ),
    ]
