# Generated by Django 3.0.7 on 2020-07-15 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AVShop', '0007_auto_20200709_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
