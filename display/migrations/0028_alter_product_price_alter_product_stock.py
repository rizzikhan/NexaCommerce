# Generated by Django 4.2 on 2025-01-02 13:33

import display.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("display", "0027_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                validators=[display.models.validate_positive],
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(
                default=0, validators=[display.models.validate_positive]
            ),
        ),
    ]
