# Generated by Django 4.1.7 on 2023-03-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_iteration_convergevalue"),
    ]

    operations = [
        migrations.AddField(
            model_name="iteration",
            name="allMatrices",
            field=models.CharField(default="", max_length=1000),
        ),
    ]