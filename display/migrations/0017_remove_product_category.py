# Generated by Django 5.1.3 on 2024-12-22 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("display", "0016_alter_product_category_delete_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
    ]
