# Generated by Django 4.2.8 on 2023-12-29 15:23

from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_field', image_cropping.fields.ImageCropField(upload_to='image/')),
                ('cropping', image_cropping.fields.ImageRatioField('image_field', '120x100', adapt_rotation=False, allow_fullsize=True, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping')),
                ('cropping_free', image_cropping.fields.ImageRatioField('image_field', '300x230', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping free')),
            ],
        ),
        migrations.AlterField(
            model_name='piece',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('image', '500x500', adapt_rotation=False, allow_fullsize=False, free_crop=True, help_text=None, hide_image_field=False, size_warning=True, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='piece',
            name='image',
            field=image_cropping.fields.ImageCropField(blank=True, upload_to='uploaded_images'),
        ),
        migrations.CreateModel(
            name='ImageFK',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cropping', image_cropping.fields.ImageRatioField('image__image_field', '120x100', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.image')),
            ],
        ),
    ]