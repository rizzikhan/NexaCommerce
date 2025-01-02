
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0002_alter_cart_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderdone",
            name="order_id",
            field=models.CharField(default=2222, editable=False, max_length=20),
            preserve_default=False,
        ),
    ]
