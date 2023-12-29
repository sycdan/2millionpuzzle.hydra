# Generated by Django 4.2.8 on 2023-12-31 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_piece_options_rename_ord_piece_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='piece',
            name='heads',
        ),
        migrations.RemoveField(
            model_name='piece',
            name='style',
        ),
        migrations.AddField(
            model_name='cell',
            name='turns',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]