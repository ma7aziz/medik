# Generated by Django 3.1.5 on 2021-02-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_product_product_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]