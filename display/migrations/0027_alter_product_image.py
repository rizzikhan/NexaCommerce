# Generated by Django 4.2 on 2024-12-30 09:30

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("display", "0026_rename_local_image_product_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="product_image"
            ),
        ),
    ]
