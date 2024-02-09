# Generated by Django 5.0.1 on 2024-02-06 17:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, unique=True, verbose_name='Опрос')),
                ('users_count', models.IntegerField(default=0, verbose_name='Количество участвовавших пользователей')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, unique=True, verbose_name='Вопрос')),
                ('first_question', models.BooleanField(default=False, verbose_name='Является ли первым вопросом в опросе')),
                ('users_answered_count', models.IntegerField(default=0, verbose_name='Количество ответивших пользователей')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.poll', verbose_name='Опрос')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, verbose_name='Вариант')),
                ('next_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.question', verbose_name='Следующий вопрос')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='polls.question', verbose_name='Вопрос')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, verbose_name='Имя пользователя')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.choice', verbose_name='Вариант')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question', verbose_name='Вопрос')),
            ],
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.UniqueConstraint(fields=('poll', 'text'), name='unique_poll_title'),
        ),
        migrations.AddConstraint(
            model_name='choice',
            constraint=models.UniqueConstraint(fields=('question', 'text'), name='unique_question_text'),
        ),
    ]
