# Generated by Django 4.1 on 2023-03-28 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "cinema_Ebooking",
            "0015_movieshowtime_movietime_promotion_schedulemovie_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="poster",
            field=models.URLField(default="", max_length=300),
        ),
    ]