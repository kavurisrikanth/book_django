# Generated by Django 2.0.3 on 2018-03-30 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0011_auto_20180330_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
