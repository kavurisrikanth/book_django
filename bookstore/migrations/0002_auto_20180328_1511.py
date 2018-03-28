# Generated by Django 2.0.3 on 2018-03-28 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AddField(
            model_name='book',
            name='isbn',
            field=models.CharField(default='isbnPlaceholder', max_length=15, primary_key=True, serialize=False),
        ),
    ]
