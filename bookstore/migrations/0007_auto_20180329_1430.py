# Generated by Django 2.0.3 on 2018-03-29 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0006_auto_20180329_1032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(default='authorPlaceholder', max_length=100),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
