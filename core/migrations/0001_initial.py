# Generated by Django 5.0 on 2024-01-02 08:33

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CowBreed",
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
                    "name",
                    models.CharField(
                        choices=[
                            ("Friesian", "Friesian"),
                            ("Sahiwal", "Sahiwal"),
                            ("Jersey", "Jersey"),
                            ("Guernsey", "Guernsey"),
                            ("Crossbreed", "Crossbreed"),
                            ("Ayrshire", "Ayrshire"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Inseminator",
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
                ("first_name", models.CharField(max_length=20)),
                ("last_name", models.CharField(max_length=20)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=15, region=None, unique=True
                    ),
                ),
                (
                    "sex",
                    models.CharField(
                        choices=[("Male", "Male"), ("Female", "Female")], max_length=6
                    ),
                ),
                ("company", models.CharField(max_length=50, null=True)),
                (
                    "license_number",
                    models.CharField(max_length=25, null=True, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cow",
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
                ("name", models.CharField(max_length=35)),
                ("date_of_birth", models.DateField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("Male", "Male"), ("Female", "Female")], max_length=6
                    ),
                ),
                (
                    "availability_status",
                    models.CharField(
                        choices=[
                            ("Alive", "Alive"),
                            ("Sold", "Sold"),
                            ("Dead", "Dead"),
                        ],
                        default="Alive",
                        max_length=5,
                    ),
                ),
                (
                    "current_pregnancy_status",
                    models.CharField(
                        choices=[
                            ("Open", "Open"),
                            ("Pregnant", "Pregnant"),
                            ("Calved", "Calved"),
                            ("Unavailable", "Unavailable"),
                        ],
                        default="Unavailable",
                        max_length=12,
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Calf", "Calf"),
                            ("Weaner", "Weaner"),
                            ("Heifer", "Heifer"),
                            ("Bull", "Bull"),
                            ("Milking Cow", "Milking Cow"),
                        ],
                        default="Calf",
                        max_length=11,
                    ),
                ),
                (
                    "current_production_status",
                    models.CharField(
                        choices=[
                            ("Open", "Open"),
                            ("Pregnant not Lactating", "Pregnant Not Lactating"),
                            ("Pregnant and Lactating", "Pregnant And Lactating"),
                            ("Dry", "Dry"),
                            ("Culled", "Culled"),
                            ("Quarantined", "Quarantined"),
                            ("Bull", "Bull"),
                            ("Young Bull", "Young Bull"),
                            ("Young Heifer", "Young Heifer"),
                            ("Mature Bull", "Mature Bull"),
                            ("Calf", "Calf"),
                            ("Weaner", "Weaner"),
                        ],
                        default="Calf",
                        max_length=22,
                    ),
                ),
                ("is_bought", models.BooleanField(default=False)),
                ("date_introduced_in_farm", models.DateField(auto_now=True)),
                ("date_of_death", models.DateField(null=True)),
                (
                    "dam",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="calves",
                        to="core.cow",
                    ),
                ),
                (
                    "sire",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="offspring",
                        to="core.cow",
                    ),
                ),
                (
                    "breed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="cows",
                        to="core.cowbreed",
                    ),
                ),
            ],
        ),
    ]
