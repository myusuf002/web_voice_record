# Generated by Django 3.0.2 on 2020-03-20 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speak', '0012_auto_20200224_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utterance', models.CharField(blank=True, max_length=512, null=True)),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('gender', models.CharField(blank=True, max_length=512, null=True)),
                ('age', models.CharField(blank=True, max_length=512, null=True)),
                ('ethnic', models.CharField(blank=True, max_length=512, null=True)),
                ('dialect', models.CharField(blank=True, max_length=512, null=True)),
                ('audio', models.FileField(upload_to='audio/')),
                ('count_good', models.BigIntegerField(blank=True, default=0, null=True)),
                ('count_bad', models.BigIntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
