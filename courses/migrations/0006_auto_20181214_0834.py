# Generated by Django 2.1.4 on 2018-12-14 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_quiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('prompt', models.TextField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Quiz'),
        ),
    ]
