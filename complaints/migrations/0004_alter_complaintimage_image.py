# Generated by Django 5.0.3 on 2025-03-03 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0003_alter_complaintimage_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaintimage',
            name='image',
            field=models.ImageField(upload_to='complaints/images/'),
        ),
    ]
