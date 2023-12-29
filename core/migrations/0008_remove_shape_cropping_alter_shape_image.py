# Generated by Django 4.2.8 on 2023-12-31 05:52

from django.db import migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_shape_alter_piece_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shape',
            name='cropping',
        ),
        migrations.AlterField(
            model_name='shape',
            name='image',
            field=image_cropping.fields.ImageCropField(blank=True, upload_to='shapes'),
        ),
    ]