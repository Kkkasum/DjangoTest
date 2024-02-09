from django.db import connection


def get_all_participants(poll_id: int) -> int:
    # Общее кол-во участников опроса
    with connection.cursor() as cur:
        query = f"""
            SELECT
              users_count
            FROM
              polls_poll
            WHERE
              id = {poll_id}
        """
        cur.execute(query)
        row = cur.fetchone()

    return row[0]


def get_answered_part(question_id: int) -> tuple[int, float]:
    # Количество ответивших и их доля от общего кол-ва участников опроса
    with connection.cursor() as cur:
        query = f"""
            SELECT
              poll_id,
              users_answered_count
            FROM
              polls_question
            WHERE
              id = {question_id}
        """
        cur.execute(query)
        row = cur.fetchone()

        users_count = get_all_participants(row[0])
        users_answered_count = row[1]

    return users_answered_count, users_answered_count / users_count * 100


def get_ordered_question_id(question_id: int) -> int:
    # Порядковый номер вопроса по кол-ву ответивших. Если кол-во совпадает, то и номер должен совпадать
    with connection.cursor() as cur:
        query = """
            SELECT
              id,
              DENSE_RANK() OVER (ORDER BY users_answered_count DESC)
            FROM
              polls_question
        """
        cur.execute(query)
        rows = cur.fetchall()

    ordered_question_id = [row[1] for row in rows if row[0] == question_id][0]

    return ordered_question_id


def get_choices_stats(question_id: int) -> list[tuple[str, int, int]]:
    # Количество ответивших на каждый из вариантов ответа и их доля от общего кол-ва ответивших
    # на этот вопрос после завершения опроса
    with connection.cursor() as cur:
        query = f"""
            SELECT
              text,
              COUNT(choice_id)
            FROM
              polls_choice t1
              LEFT JOIN polls_answer t2
                ON t1.id = t2.choice_id
            WHERE
              t1.question_id = {question_id}
            GROUP BY
              t1.id
        """

        cur.execute(query)
        rows = cur.fetchall()

    return rows


# Каждая функция отвечает за одно определенное действие (принцип единственной ответственности)
def get_choices_stats_formatted(question_id: int) -> list[tuple[str, int, int]]:
    rows = get_choices_stats(question_id)
    users_answered_count = get_answered_part(question_id)[0]

    choices_stats = []
    for row in rows:
        # если количество ответивших равно 0, то процент зануляется
        if not users_answered_count:
            choices_count_percent = 0
        else:
            choices_count_percent = round(row[1] / users_answered_count * 100)
        choices_stats.append((row[0], row[1], choices_count_percent))

    return choices_stats
