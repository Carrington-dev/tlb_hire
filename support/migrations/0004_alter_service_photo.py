# Generated by Django 4.1.7 on 2023-03-10 13:48

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_service_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='photo',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], force_format=None, keep_meta=True, quality=0, size=[1024, 768], upload_to='services/photo'),
        ),
    ]