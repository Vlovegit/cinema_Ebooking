# Generated by Django 4.1.7 on 2023-04-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_Ebooking', '0024_tickets_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='status',
            field=models.TextField(blank=True, default='Active', null=True),
        ),
    ]
