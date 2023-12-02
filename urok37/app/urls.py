from django.urls import path
from .views import *

urlpatterns = [
    path('home/', display_home_page, name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', perform_logout, name='logout'),
    path('register/', UserSignupView.as_view(), name='register'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile'),
    path('change_password/', UserPasswordUpdateView.as_view(), name='change_password'),
    path('edit_profile/<int:user_id>/', UserProfileEditView.as_view(), name='edit_profile'),
    path('add_question/', QuestionCreationView.as_view(), name='add_question'),
    path('quiz/', CharacterQuizView.as_view(), name='quiz'),
]
