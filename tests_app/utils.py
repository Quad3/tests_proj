from random import shuffle

from .models import Question


def retrieve_random_questions(quantity: int):
    if quantity < 1:
        raise BaseException('Количество вопросов меньше 1.')
    
    question_ids = list(Question.objects.values_list('id', flat=True))
    if quantity > len(question_ids):
        raise BaseException('Количество вопросов слишком большое')

    shuffle(question_ids)
    random_questions = Question.objects.select_related('theme').filter(id__in=question_ids[:quantity])
    return random_questions.order_by('?')
