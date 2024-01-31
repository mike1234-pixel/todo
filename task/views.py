from django.shortcuts import render

from .forms import NewTaskForm
from .models import Task

# Create your views here.

def index(request):
    tasks = Task.objects.all()

    return render(request, 'task/index.html', {'tasks': tasks})

def detail(request, pk):
    task = Task.objects.get(pk=pk)

    return render(request, 'task/detail.html', {'task': task})

def new(request):
    form = NewTaskForm
    return render(request, 'task/new.html', {'form': form})