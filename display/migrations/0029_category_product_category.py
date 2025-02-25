# Generated by Django 4.2 on 2025-01-03 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("display", "0028_alter_product_price_alter_product_stock"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="display.category",
            ),
        ),
    ]
