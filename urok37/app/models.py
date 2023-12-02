from django.db import models
from django.contrib.auth.models import AbstractUser, make_password


# Create your models here.


class User(AbstractUser):
    Passed_Tests = models.PositiveIntegerField(default=0)
    Correct_Answers = models.PositiveIntegerField(default=0)
    Wrong_Answers = models.PositiveIntegerField(default=0)
    Perfect_Tests = models.PositiveIntegerField(default=0)
    Successes_Rate = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:  # Check if the user is being created (not updating)
            self.set_password(self.password)

        try:
            self.Successes_Rate = self.Correct_Answers / (self.Correct_Answers + self.Wrong_Answers)
        except ZeroDivisionError:
            self.Successes_Rate = 0

        super(User, self).save(*args, **kwargs)


class Question(models.Model):
    image = models.ImageField(upload_to='images/')
    right_answer = models.CharField(max_length=256)
    wrong_answer_1 = models.CharField(max_length=256)
    wrong_answer_2 = models.CharField(max_length=256)
    wrong_answer_3 = models.CharField(max_length=256)
    wrong_answer_4 = models.CharField(max_length=256)
    likes_count = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.right_answer


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.question.right_answer}"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.question.likes_count += 1
        self.question.save()
        return super(Like, self).save(force_insert, force_update, using, update_fields)


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    right_answers = models.PositiveIntegerField()
    wrong_answers = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.right_answers} - {self.wrong_answers}"
