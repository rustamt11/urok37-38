from django import template
import random

register = template.Library()


@register.filter(name='get_random_answers')
def get_random_answers(question):
    answers = [question.right_answer, question.wrong_answer_1, question.wrong_answer_2, question.wrong_answer_3,
               question.wrong_answer_4]
    random.shuffle(answers)
    return answers
