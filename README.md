### Dependencies
Используется poetry (https://python-poetry.org) в качестве менеджера пакетов.
```
poetry install
```

## Cоздание сервиса опросов с учетом пользователя и динамическим отображением вопросов.
- Создание и редактирование опросов и вопросов через админку ✅
- Реализацию веб-интерфейса, позволяющего пользователям проходить опросы и отвечать на вопросы ✅
- Сохранение ответов пользователей в связке с соответствующими опросами ✅
- Логику, позволяющую определить, какие вопросы показывать или скрывать в зависимости от предыдущих ответов пользователя ✅
В таблице Choices (Варианты) есть поле next_question, которое указывает на вопрос, который должен следовать при выборе
данного варианта. Таким образом, можно реализовать ветвление опроса
- Вывод результатов опросов, включая статистику ответов на каждый вопрос, после завершения опроса ✅ 

Реализовать с помощью минимального кол-ва SQL-запросов без использования ORM (все запросы хранятся в файле database/queries.py):
- Общее кол-во участников опроса (get_all_participants) ✅
- Кол-во ответивших и их доля от общего кол-ва участников опроса (get_answered_part) ✅
- Порядковый номер вопроса по кол-ву ответивших. Если кол-во совпадает, то и номер должен совпадать (get_ordered_question_id) ✅
- Кол-во ответивших на каждый из вариантов ответа и их доля от общего кол-ва ответивших на этот вопрос после завершения опроса (get_choices_stats, get_choices_stats_formatted) ✅