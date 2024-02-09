from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Poll(models.Model):
    title = models.CharField(max_length=256, verbose_name='Опрос', unique=True)
    users_count = models.IntegerField(default=0, verbose_name='Общее количество участников опроса')

    def __str__(self):
        return self.title


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Опрос')
    text = models.CharField(max_length=256, verbose_name='Вопрос', unique=True)
    first_question = models.BooleanField(default=False, verbose_name='Является ли первым вопросом в опросе')
    users_answered_count = models.IntegerField(default=0, verbose_name='Количество ответивших пользователей')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['poll', 'text'], name='unique_poll_title')
        ]

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question', verbose_name='Вопрос')
    text = models.CharField(max_length=256, verbose_name='Вариант')
    next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='Следующий вопрос'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'text'], name='unique_question_text')
        ]

    def __str__(self):
        return self.text


class Answer(models.Model):
    username = models.CharField(max_length=64, verbose_name='Имя пользователя')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name='Вариант')


# если в Question уже существует объект со значением poll=instance.poll.id и first_question=True,
# то значение поля first_question добавляемого экземпляра устанавливается в значение False
@receiver(pre_save, sender=Question)
def check_unique_first_question(sender: models.base.ModelBase, instance: Question, **kwargs):
    if instance.first_question:
        first_question = Question.objects.filter(poll=instance.poll.id, first_question=True).first()

        if first_question and instance != first_question:
            instance.first_question = False
