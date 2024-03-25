from typing import Any

from django.views.generic import DetailView, ListView
from assignable.models import Task


class TaskListView(ListView):
    queryset = Task.objects.all()
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    queryset = Task.objects.all()
    context_object_name = "task"
