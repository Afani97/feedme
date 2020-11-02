from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from ..models import Meal, Eater
from django.db.models import Q


@login_required
def home(request):
    if hasattr(request.user, 'eater'):
        meals = Meal.objects.filter(eater=request.user.eater).order_by('-created_at')[:10]
        not_started_meals = [m for m in meals if m.status == "ns"]
        meals_in_progress = [m for m in meals if m.status == "bp" or
                             m.status == "ad" or
                             m.status == "er"]
        finished_meals = [m for m in meals if m.status == "fi"]
        context = {
            'not_started_meals': not_started_meals,
            'meals_in_progress': meals_in_progress,
            'finished_meals': finished_meals
        }
        return render(request, 'fm/eater_home.html', context)
    elif hasattr(request.user, 'cook'):
        meals = Meal.objects.filter(~Q(status="fi")).order_by('-created_at')
        not_started_meals = [m for m in meals if m.status == "ns"]
        meals_in_progress = [m for m in meals if m.status == "bp" or m.status == "ad"]
        meals_en_route = [m for m in meals if m.status == "er"]
        context = {
            'not_started_meals': not_started_meals,
            'meals_in_progress': meals_in_progress,
            'meals_en_route': meals_en_route
        }
        return render(request, 'fm/cook_home.html', context)
    return redirect(reverse('login'))
