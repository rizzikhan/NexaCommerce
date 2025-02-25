# Generated by Django 4.2 on 2024-12-30 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("display", "0021_alter_product_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="image",
            new_name="cloud_image",
        ),
        migrations.AddField(
            model_name="product",
            name="local_image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
