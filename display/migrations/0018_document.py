# Generated by Django 4.2 on 2024-12-28 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("display", "0017_remove_product_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pdf_file", models.FileField(upload_to="uploads/")),
                ("processed", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
