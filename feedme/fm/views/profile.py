from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from ..forms import EditCookForm, EditEaterForm
from ..models import Meal, Cook, Eater
import base64


@login_required
def profile(request):
    context = {}
    if hasattr(request.user, 'eater'):
        context = {
            'profile': request.user.eater,
            'type': 'eater'
        }
        if request.user.eater.profile_image:
            context['profile_image'] = base64.b64encode(request.user.eater.profile_image).decode()
        try:
            context['favorite_meal'] = Meal.objects.get(pk=request.user.eater.favorite_meal)
        except Meal.DoesNotExist:
            pass
    elif hasattr(request.user, 'cook'):
        context = {
            'profile': request.user.cook,
            'type': 'cook',
        }
        if request.user.cook.profile_image:
            context['profile_image'] = base64.b64encode(request.user.cook.profile_image).decode()
    return render(request, 'fm/profile/profile.html', context)


@method_decorator(login_required, name='dispatch')
class CookProfileForm(UpdateView):
    model = Cook
    form_class = EditCookForm
    template_name = 'fm/profile/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_initial(self):
        return {'email': self.request.user.email,
                'profile_image': ""}

    def get_object(self):
        return self.request.user.cook

    def get_form(self):
        form = super(CookProfileForm, self).get_form(EditCookForm)
        form.user = self.request.user
        return form

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        current_user = self.request.user
        current_user.first_name = form.cleaned_data.get('name')
        current_user.username = email
        current_user.cook.profile_image = form.cleaned_data.get('profile_image')
        current_user.email = email
        current_user.save()
        return redirect(reverse_lazy('profile'))


@method_decorator(login_required, name='dispatch')
class EaterProfileForm(UpdateView):
    model = Eater
    form_class = EditEaterForm
    template_name = 'fm/profile/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_initial(self):
        context = {'email': self.request.user.email,
                   'profile_image': ""}
        if self.request.user.eater.address.all().first():
            context['address_string'] = self.request.user.eater.address.all().first()
        return context

    def get_object(self):
        return self.request.user.eater

    def get_form(self):
        form = super(EaterProfileForm, self).get_form(EditEaterForm)
        form.user = self.request.user
        return form

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        current_user = self.request.user
        current_user.first_name = form.cleaned_data.get('name')
        current_user.username = email
        current_user.email = email
        current_user.eater.profile_image = form.cleaned_data.get('profile_image')
        current_user.eater.address.clear()
        current_user.eater.address.add(form.cleaned_data.get('address_string'))
        current_user.eater.save()
        current_user.save()
        return redirect(reverse_lazy('profile'))