# Generated by Django 5.0.6 on 2024-07-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_alter_pet_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='adopted',
            field=models.BooleanField(default=False),
        ),
    ]
