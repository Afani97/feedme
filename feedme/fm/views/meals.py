from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, UpdateView

from ..forms import NewMealForm
from ..models import Meal


@method_decorator(login_required, name='dispatch')
class NewMealView(CreateView):
    model = Meal
    form_class = NewMealForm
    template_name = 'fm/meals/new.html'

    def form_valid(self, form):
        meal = form.save()
        current_user = self.request.user.eater
        current_user.meals.add(meal)
        current_user.save()
        return redirect(reverse_lazy('home'))


@method_decorator(login_required, name='dispatch')
class EditMealView(UserPassesTestMixin, UpdateView):
    model = Meal
    form_class = NewMealForm
    template_name = 'fm/meals/edit.html'

    def form_valid(self, form):
        meal = form.save()
        current_user = self.request.user.eater
        current_user.meals.add(meal)
        current_user.save()
        return redirect(reverse_lazy('profile'))

    def test_func(self):
        obj = self.get_object()
        return hasattr(self.request.user, 'eater') and obj in self.request.user.eater.meals.all()

    def handle_no_permission(self):
        return redirect(reverse_lazy('home'))


@method_decorator(login_required, name='dispatch')
class DeleteMealView(UserPassesTestMixin, DeleteView):
    template_name = 'fm/meals/delete.html'
    model = Meal
    success_url = reverse_lazy('profile')

    def test_func(self):
        obj = self.get_object()
        return hasattr(self.request.user, 'eater') and obj in self.request.user.eater.meals.all()

    def handle_no_permission(self):
        return redirect(reverse_lazy('home'))


@login_required
def favorite_meal(request, meal_id):
    meal = Meal.objects.get(pk=meal_id)
    if meal:
        current_eater = request.user.eater
        current_eater.favorite_meal = meal.id
        current_eater.save()
    return redirect(reverse_lazy('home'))


@login_required
def view_meal(request, meal_id):
    meal = Meal.objects.get(pk=meal_id)
    context = {'meal': meal}
    if meal:
        if hasattr(request.user, 'eater') and meal in request.user.eater.meals.all():
            context['show_edit'] = True
        return render(request, 'fm/meals/view.html', context)
    return redirect(reverse_lazy('home'))


@login_required
def start_cooking_meal(request, meal_id):
    if hasattr(request.user, 'cook'):
        meal = Meal.objects.get(pk=meal_id)
        if meal:
            meal.status = "bp"
            meal.save()
    return redirect(reverse_lazy('home'))


@method_decorator(login_required, name='dispatch')
class UpdateMealStatus(UserPassesTestMixin, UpdateView):
    model = Meal
    fields = ('status',)
    template_name = 'fm/meals/update_status.html'

    def form_valid(self, form):
        form.save()
        return redirect(reverse_lazy('home'))

    def test_func(self):
        return hasattr(self.request.user, 'cook')

    def handle_no_permission(self):
        return redirect(reverse_lazy('home'))