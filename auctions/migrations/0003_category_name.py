# Generated by Django 3.0.3 on 2020-08-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200830_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.TextField(default='No Category', max_length=64),
        ),
    ]
