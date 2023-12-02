from .models import Question


class QuestionViewsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200 and 'text/html' in response['Content-Type']:
            try:
                question_id = list(request.GET.get('question_id'))
                for question in question_id:
                    question = Question.objects.get(id=question)
                    question.views += 1
                    question.save()

            except Exception:
                pass
        return response
