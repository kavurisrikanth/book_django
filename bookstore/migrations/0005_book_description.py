# Generated by Django 2.0.3 on 2018-03-28 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_auto_20180328_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.CharField(default='descriptionPlaceholder', max_length=2000),
        ),
    ]