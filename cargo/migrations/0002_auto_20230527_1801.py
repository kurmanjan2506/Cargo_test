# Generated by Django 3.2.15 on 2023-05-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargo',
            options={'verbose_name': 'Груз', 'verbose_name_plural': 'Грузы'},
        ),
        migrations.AlterModelOptions(
            name='cars',
            options={'verbose_name': 'Машина', 'verbose_name_plural': 'Машины'},
        ),
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name': 'Локация', 'verbose_name_plural': 'Локации'},
        ),
        migrations.AlterField(
            model_name='cars',
            name='unique_num',
            field=models.CharField(default='9364A', max_length=5, unique=True),
        ),
    ]
