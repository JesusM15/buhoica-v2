# Generated by Django 4.1.4 on 2022-12-23 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0004_digital_slug_fisico_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='digital',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=100000),
        ),
        migrations.AlterField(
            model_name='fisico',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=100000),
        ),
    ]