import random

from django.views.generic.base import ContextMixin
from .models import User


class TestMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = User.objects.get(username=self.request.user)
            context['test_statistics'] = {
                'passed_tests': user.Passed_Tests,
                'correct_answers': user.Correct_Answers,
                'wrong_answers': user.Wrong_Answers,
                'perfect_tests': user.Perfect_Tests,
            }
        return context
