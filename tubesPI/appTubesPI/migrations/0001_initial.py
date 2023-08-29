# Generated by Django 4.2.1 on 2023-05-16 09:08

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="kain",
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
                ("name", models.CharField(max_length=50)),
                ("desc", models.TextField()),
                ("img", models.TextField()),
                ("lowest_est", models.CharField(max_length=10)),
                ("highest_est", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="list_toko",
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
                ("nama_toko", models.CharField(max_length=50)),
                ("lokasi", models.CharField(max_length=50)),
                ("jam_operasional", models.CharField(max_length=50)),
                # ("contact_person", models.CharField(max_length=20, unique=True)),
                ("contact_person", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="detail_toko",
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
                ("harga", models.BigIntegerField()),
                (
                    "id_kain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appTubesPI.kain",
                    ),
                ),
                (
                    "id_toko",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="appTubesPI.list_toko",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="User",
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
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                # ("email", models.EmailField(max_length=100, unique=True)),
                # ("username", models.CharField(max_length=50, unique=True)),
                ("email", models.EmailField(max_length=100)),
                ("username", models.CharField(max_length=50)),
                # ("password", models.CharField(max_length=100, null=True)),
                ("password", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=255)),
                (
                    "level",
                    models.CharField(
                        choices=[
                            ("2", "Super Admin"),
                            ("1", "Admin"),
                            ("0", "Customer"),
                        ],
                        default="0",
                        max_length=1,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "ordering": ("level",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
