# Generated by Django 3.0.7 on 2020-07-09 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AVShop', '0006_auto_20200709_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]