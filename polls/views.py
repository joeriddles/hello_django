from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self) -> QuerySet[Question]:
        """Retrusn the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


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
