# Generated by Django 3.2.4 on 2021-06-15 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Template",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, default="")),
                ("process_setting", models.JSONField(blank=True, null=True)),
                ("signal_setting", models.JSONField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Tenant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("external_tenant", models.CharField(max_length=32, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Workflow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True, default="")),
                ("group_refs", models.JSONField(default=list)),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="approval.template",
                    ),
                ),
                (
                    "tenant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="approval.tenant",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="template",
            name="tenant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="approval.tenant"
            ),
        ),
        migrations.AddConstraint(
            model_name="workflow",
            constraint=models.CheckConstraint(
                check=models.Q(("name__length__gt", 0)),
                name="approval_workflow_name_empty",
            ),
        ),
        migrations.AddConstraint(
            model_name="workflow",
            constraint=models.UniqueConstraint(
                fields=("name", "tenant", "template"),
                name="approval_workflow_name_unique",
            ),
        ),
        migrations.AddConstraint(
            model_name="template",
            constraint=models.CheckConstraint(
                check=models.Q(("title__length__gt", 0)),
                name="approval_template_title_empty",
            ),
        ),
        migrations.AddConstraint(
            model_name="template",
            constraint=models.UniqueConstraint(
                fields=("title", "tenant"), name="approval_template_title_unique"
            ),
        ),
    ]
