# Generated by Django 3.2.15 on 2023-05-28 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0005_alter_car_unique_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='unique_num',
            field=models.CharField(default='5078N', max_length=5, unique=True),
        ),
    ]