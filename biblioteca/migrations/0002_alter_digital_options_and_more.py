# Generated by Django 4.1.4 on 2022-12-23 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='digital',
            options={'verbose_name_plural': 'Digitales'},
        ),
        migrations.RenameField(
            model_name='fisico',
            old_name='link_compra',
            new_name='link_de_compra',
        ),
    ]