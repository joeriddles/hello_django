from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from polls.models import Choice, Question


def index(request: HttpRequest) -> HttpResponse:
    latest_questions = Question.objects.order_by("-pub_date")[:5]
    context = { "latest_questions": latest_questions }
    return render(request, "polls/index.html", context)


def detail(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", { "question": question })


def vote(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    try:
        post_choice: str = request.POST["choice"]
        selected_choice: Choice = question.choice_set.get(pk=post_choice)  # type: ignore
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))  # type: ignore


def results(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", { "question": question })
