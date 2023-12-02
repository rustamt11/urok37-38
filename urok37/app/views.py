import random
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from .forms import *
from .models import *
from django.core.cache import cache


# Create your views here.

def display_home_page(request):
    return render(request, 'index.html')


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomAuthenticationForm  # Проверьте правильность имени формы
    next_page = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        if 'test_results' in cache:
            test_results = cache.get('test_results')
            user.Passed_Tests += test_results.get('passed_tests', 0)
            user.Correct_Answers += test_results.get('correct_answers', 0)
            user.Wrong_Answers += test_results.get('wrong_answers', 0)
            cache.delete('test_results')
        user.save()

        return response


class UserSignupView(CreateView):
    model = User
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')


class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'
    pk_url_kwarg = 'user_id'


def perform_logout(request):
    logout(request)
    return redirect('home')


class UserPasswordUpdateView(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('home')


class UserProfileEditView(UpdateView):
    model = User
    template_name = 'change_profile.html'
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'user_id'


class QuestionCreationView(CreateView):
    model = Question
    template_name = 'add_question.html'
    form_class = NewQuestionForm
    success_url = reverse_lazy('home')


test_questions = []


class CharacterQuizView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        questions = list(Question.objects.all())
        global test_questions

        if len(questions) < 10:
            test_questions = questions
            random.shuffle(test_questions)
        else:
            test_questions = random.sample(questions, 10)

        context['quiz_questions'] = test_questions
        return context

    def post(self, request, *args, **kwargs):
        if 'like_question' in request.POST:
            self.handle_like(request)
        return self.evaluate_answers(request)

    def handle_like(self, request):
        if request.user.is_authenticated:
            question_id = request.POST.get('like')
            question = get_object_or_404(Question, id=question_id)
            like, created = Like.objects.get_or_create(user=request.user, question=question)

            if not created:
                question.likes_count -= 1
                like.delete()

            question.save()

    def evaluate_answers(self, request):
        right_answers = 0
        wrong_answers = 0
        perfect_test = False

        global test_questions
        print(test_questions)
        for question in test_questions:
            if question.right_answer == request.POST.get(f"answers_{question.id}"):
                right_answers += 1
            else:
                wrong_answers += 1

        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            user.Passed_Tests += 1
            user.Correct_Answers += right_answers
            user.Wrong_Answers += wrong_answers

            if len(test_questions) == 10:
                if right_answers >= 7:
                    user.Perfect_Tests += 1
                    perfect_test = True
            else:
                if right_answers >= len(test_questions) // 2:
                    user.Perfect_Tests += 1
                    perfect_test = True

            test_results = {
                'right_answers': right_answers,
                'wrong_answers': wrong_answers,
                'perfect_test': perfect_test,
            }
            cache.set(f'test_results_{user.username}', test_results)
            user.save()

        else:
            test_results = {
                'right_answers': right_answers,
                'wrong_answers': wrong_answers,
                'perfect_test': right_answers == len(test_questions),
            }
            cache.set(f'test_results', test_results)
        print(test_questions)
        next_question_url = reverse('test') + f'?question_id={",".join(str(elem.id) for elem in test_questions)}'
        return redirect(next_question_url)
