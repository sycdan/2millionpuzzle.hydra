# Generated by Django 4.2.8 on 2024-01-03 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_cell_created_cell_modified_piece_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shape',
            name='heads',
            field=models.CharField(blank=True, default='', help_text='Some combination of n|e|s|w', max_length=255),
        ),
    ]
