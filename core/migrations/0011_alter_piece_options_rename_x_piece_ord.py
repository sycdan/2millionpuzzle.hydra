# Generated by Django 4.2.8 on 2023-12-31 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_cell_shape'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='piece',
            options={'ordering': ('shape', 'ord')},
        ),
        migrations.RenameField(
            model_name='piece',
            old_name='x',
            new_name='ord',
        ),
    ]
