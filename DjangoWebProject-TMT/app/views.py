"""
Definition of views.
"""

from asyncio import Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from app.templates.app.forms import RegisterUserForm
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.core import serializers
import json


# home page
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def task_json(request):
    # Query the database for all tasks
    tasks = Task.objects.filter(user=request.user)

    # Serialize the tasks into JSON format
    task_list = serializers.serialize('json', tasks)

    # Convert the JSON string into a list
    task_list = json.loads(task_list)

    # Return the tasks in a JsonResponse
    return JsonResponse(task_list, safe=False)


# signup page
def user_signup(request):
    """Renders the signup page."""
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(
        request,
        'app/signup.html',
        {
            'title': 'User registration',
            'form': form,
            'year': datetime.now().year,
        }
    )


# task list
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # The TaskList is bound to the user who is logged in
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        # Group tasks by status
        context['tasks_by_status'] = {
            'TO DO': context['tasks'].filter(status='TO DO'),
            'IN PROGRESS': context['tasks'].filter(status='IN PROGRESS'),
            'BLOCKED': context['tasks'].filter(status='BLOCKED'),
            'DONE': context['tasks'].filter(status='DONE'),
        }

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input)

        context['search_input'] = search_input
        context['count'] = context['tasks'].filter(complete=False).count()

        dates = context['tasks'].dates('due_date', 'day')
        tasks_by_date = {date: context['tasks'].filter(
            due_date=date).order_by('-priority') for date in dates}
        context['tasks_by_date'] = tasks_by_date

        return context

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-due_date', '-priority')


class TaskBoardView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'app/task_board.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)

        # Group tasks by status
        context['tasks_by_status'] = {
            'TO DO': context['tasks'].filter(status='TO DO'),
            'IN PROGRESS': context['tasks'].filter(status='IN PROGRESS'),
            'BLOCKED': context['tasks'].filter(status='BLOCKED'),
            'DONE': context['tasks'].filter(status='DONE'),
        }

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'app/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    template_name = 'app/task_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'app/task_form.html'
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
