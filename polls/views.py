# Django imports
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django.views import View

# Poll imports
from polls.models import Poll, Choice

# Create your views here.
def index(request):
    return HttpResponse("You're at the polls index.")

def view_poll(request, id):
    return HttpResponse("You're viewing poll %s." % id)

def create_poll(request):
    if request.method == "POST":
        # Get poll question & answers
        question = request.POST.get("question")
        answers = request.POST.get("answers")
        # Create poll with choices
        new_poll = Poll(question=question, answers=answers, reward=100, date=timezone.now())
        new_poll.save()