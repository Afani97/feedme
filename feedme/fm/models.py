import uuid

from django.contrib.auth.models import User
from django.db import models

MEAL_STATES = [('ns', 'Not Started'), ('bp', 'Being Prepped'),
               ('ad', 'Almost Done'), ('fi', 'Finished'), ('er', 'En route')]


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    street_name = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=2, null=False)

    def __str__(self):
        return f"{self.street_name}, {self.city}, {self.state}"

    class Meta:
        verbose_name_plural = "Address"


class DietRestrictions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Diet Restrictions"


class FoodPreferences(models.Model):
    PRIORITY_CHOICES = [('l', 'Low'), ('h', 'High'), ('n', 'None')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='n')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Food Preferences"


class Meal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True, blank=True)
    diet_restrictions = models.ManyToManyField(DietRestrictions, blank=True)
    food_preferences = models.ManyToManyField(FoodPreferences, blank=True)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=MEAL_STATES, default='ns')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=200, null=False)
    profile_image = models.BinaryField(null=True, blank=True, editable=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Eater(Account):
    favorite_meal = models.UUIDField(null=True, blank=True)
    meals = models.ManyToManyField(Meal, blank=True)
    diet_restrictions = models.ManyToManyField(DietRestrictions, blank=True)
    food_preferences = models.ManyToManyField(FoodPreferences, blank=True)
    address = models.ManyToManyField(Address, blank=True)


class Cook(Account):
    speciality = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
