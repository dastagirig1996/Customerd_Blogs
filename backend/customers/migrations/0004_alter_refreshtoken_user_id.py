# Generated by Django 4.2 on 2024-09-22 18:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0003_refreshtoken_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="refreshtoken",
            name="user_id",
            field=models.IntegerField(),
        ),
    ]
