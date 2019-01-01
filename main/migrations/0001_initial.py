# Generated by Django 2.1.4 on 2019-01-01 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aconstraint',
            fields=[
                ('a_con_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=30)),
                ('h_quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('name', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('teacher', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('name', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('day', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('hour', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('schedule_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('day_of_week', models.PositiveIntegerField()),
                ('hour', models.PositiveIntegerField()),
                ('classroom', models.CharField(max_length=5)),
                ('teacher', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('parent1', models.CharField(max_length=30)),
                ('parent2', models.CharField(max_length=30)),
                ('classroom', models.CharField(max_length=5)),
                ('birthday', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tconstraint',
            fields=[
                ('t_con_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('teacher', models.CharField(max_length=30)),
                ('day_of_week', models.PositiveIntegerField()),
                ('hour', models.PositiveIntegerField()),
                ('priority', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Tsubject',
            fields=[
                ('t_sub_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('teacher', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=30)),
            ],
        ),
    ]
