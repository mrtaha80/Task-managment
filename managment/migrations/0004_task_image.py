# Generated by Django 4.1.5 on 2023-12-01 09:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("managment", "0003_task_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="task_images"),
        ),
    ]
