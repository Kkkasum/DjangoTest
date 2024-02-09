from django.urls import path

from .views import polls_view, start_poll_view, question_view, choice_res_view, finish_view


app_name = 'polls'
urlpatterns = [
    path('', polls_view, name='polls'),
    path('<int:poll_id>/', start_poll_view, name='start_poll'),
    path('<int:poll_id>/<int:question_id>/', question_view, name='question'),
    path('<int:poll_id>/<int:question_id>/res', choice_res_view, name='choice'),
    path('<int:poll_id>/finish', finish_view, name='finish')
]
