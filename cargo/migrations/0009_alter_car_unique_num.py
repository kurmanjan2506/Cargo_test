# Generated by Django 4.2.1 on 2023-05-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0008_alter_car_unique_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='unique_num',
            field=models.CharField(default='6401P', max_length=5, unique=True),
        ),
    ]
