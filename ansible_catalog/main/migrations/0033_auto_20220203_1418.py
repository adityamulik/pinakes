# Generated by Django 3.2.5 on 2022-02-03 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0032_auto_20220131_1610"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="portfolio",
            name="owner",
        ),
        migrations.AddField(
            model_name="portfolio",
            name="user",
            field=models.ForeignKey(
                help_text="ID of the user who created this object",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="portfolioitem",
            name="user",
            field=models.ForeignKey(
                help_text="ID of the user who created this object",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                help_text="ID of the user who created this object",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="user",
            field=models.ForeignKey(
                help_text="ID of the user who created this object",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
