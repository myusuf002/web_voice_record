# Generated by Django 3.0.2 on 2020-02-20 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speak', '0006_auto_20200220_0340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utterance',
            name='count',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
