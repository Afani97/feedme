import io

from PIL import Image
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Meal, Eater, Address, Cook, MEAL_STATES


class RegisterForm(UserCreationForm, forms.ModelForm):
    ACCOUNT_TYPES = [('e', 'Eater'), ('c', 'Cook')]
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="First name")
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES)

    class Meta:
        model = User
        fields = ("first_name", "email", 'password1',)


class LoginForm(forms.ModelForm):
    email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('email'),
                            password=self.cleaned_data.get('password'))
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('email', 'password',)


class NewMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = '__all__'
        exclude = ('status',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'diet_restrictions': 'Select which apply to you, hold crtl to select more than 1',
            'food_preferences': 'Select which apply to you, hold crtl to select more than 1',
        }


class EditEaterForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile image', required=False)
    email = forms.EmailField(label='Email',
                             required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'example@test.com'}))
    address_string = forms.CharField(label='Address',
                                     required=False,
                                     widget=forms.TextInput(attrs={'placeholder': '123 Main St, Boston, MA'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.user.email and User.objects.filter(email=email).count() != 0:
            raise ValidationError("Email already taken")
        return email

    def clean_address_string(self):
        address = self.cleaned_data.get('address_string').split(', ')
        eater_address = Address(street_name=address[0].title(),
                                city=address[1].title(),
                                state=address[2].title())
        eater_address.save()
        return eater_address

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            file_type = profile_image.image.format
            i = Image.open(profile_image)
            i.thumbnail((100, 100))
            output = io.BytesIO()
            i.save(output, format=file_type)
            return output.getvalue()
        return self.user.eater.profile_image

    class Meta:
        model = Eater
        fields = ('profile_image', 'name', 'email', 'diet_restrictions', 'food_preferences', 'address_string',)
        exclude = ('user', 'address',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3})
        }
        help_texts = {
            'diet_restrictions': 'Select which apply to you, hold crtl to select more than 1',
            'food_preferences': 'Select which apply to you, hold crtl to select more than 1',
        }


class EditCookForm(forms.ModelForm):
    profile_image = forms.ImageField(label='Profile image', required=False)
    email = forms.EmailField(label='Email',
                             required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'example@test.com'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != self.user.email and User.objects.filter(email=email).count() != 0:
            raise ValidationError("Email already taken")
        return email

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image:
            file_type = profile_image.image.format
            i = Image.open(profile_image)
            i.thumbnail((100, 100))
            output = io.BytesIO()
            i.save(output, format=file_type)
            return output.getvalue()
        return self.user.cook.profile_image

    class Meta:
        model = Cook
        fields = ('profile_image', 'name', 'email', 'speciality',)
        exclude = ('user',)
        widgets = {
            'speciality': forms.Textarea(attrs={'rows': 3}),
        }
