# Generated by Django 4.2.6 on 2024-02-07 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0004_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='county',
            field=models.CharField(choices=[('Nairobi', 'Nairobi'), ('Mombasa', 'Mombasa')], default='Nairobi', max_length=50),
        ),
    ]
