# Generated by Django 4.2.4 on 2023-08-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='address_type',
            field=models.IntegerField(choices=[(1, 'Billing Address'), (2, 'Shipping Address')], default=1, verbose_name='address type'),
        ),
    ]
