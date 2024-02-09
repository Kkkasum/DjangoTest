from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import F
from django.contrib.auth.decorators import login_required

from database.queries import get_all_participants, get_choices_stats_formatted

from .models import Poll, Question, Choice, Answer


class ChoiceFinish:
    def __init__(self, text: str, answer_count: int, answer_percent: int):
        self.text = text
        self.answer_count = answer_count
        self.answer_percent = answer_percent


def polls_view(request):
    polls = Poll.objects.all()

    return render(
        request,
        'polls/index.html',
        {
            'polls': polls
        }
    )


@login_required(login_url='login')
def start_poll_view(request, poll_id):
    # увеличиваем количество участвоваших пользователей
    Poll.objects.filter(pk=poll_id).update(users_count=F('users_count') + 1)

    # получаем первый вопрос для заданного опроса
    question = get_object_or_404(Question, poll=poll_id, first_question=True)

    return HttpResponseRedirect(reverse('polls:question', args=(poll_id, question.id,)))


def question_view(request, poll_id, question_id):
    poll = get_object_or_404(Poll, pk=poll_id)  # этот объект нужен для использования poll.title в title шаблона
    question = get_object_or_404(Question, pk=question_id)  # от этого объекта нужно поле text

    try:
        choices = Choice.objects.all().filter(question_id=question.id)
    except Choice.DoesNotExist:
        raise Http404('Для этого вопроса нет вариантов')

    # если у какого-нибудь варианта ответа нет следующего вопроса (значения в поле next_question),
    # то такой вопрос считается последним
    for choice in choices:
        if not choice.next_question:
            return render(
                request,
                'polls/last_question.html',
                {
                    'poll_title': poll.title,
                    'poll_id': poll.id,
                    'question': question,
                    'choices': choices
                }
            )

    return render(
        request,
        'polls/question.html',
        {
            'poll_title': poll.title,
            'poll_id': poll.id,
            'question': question,
            'choices': choices,
        }
    )


def choice_res_view(request, poll_id, question_id):
    question = get_object_or_404(Question, pk=question_id)  # current question
    question.users_answered_count += 1
    question.save()

    try:
        selected_choice = Choice.objects.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        choices = Choice.objects.all().filter(question_id=question_id)
        error_msg = 'Вы не выбрали вариант'
        return render(
            request,
            'polls/question.html',
            {
                'poll_id': poll_id,
                'question': question,
                'error': error_msg,
                'choices': choices
            }
        )

    answer = Answer(username=request.user.username, question=question, choice=selected_choice)
    answer.save()

    if not selected_choice.next_question:
        return HttpResponseRedirect(reverse('polls:finish', args=(poll_id,)))

    return HttpResponseRedirect(reverse('polls:question', args=(poll_id, selected_choice.next_question.id,)))


def finish_view(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = Question.objects.filter(poll=poll_id)

    questions_choices = {}
    for question in questions:
        choices_stats = get_choices_stats_formatted(question.id)
        questions_choices[question.text] = [
            ChoiceFinish(choice[0], choice[1], choice[2])
            for choice in choices_stats
        ]

    return render(
        request,
        'polls/finish.html',
        {
            'poll_title': poll.title,
            'questions': questions_choices
        }
    )
