from django.contrib import admin

# Register your models here.
from .models import Address, DietRestrictions, FoodPreferences, Meal, Eater, Cook

admin.site.register(Address)
admin.site.register(DietRestrictions)
admin.site.register(FoodPreferences)
admin.site.register(Eater)
admin.site.register(Cook)


class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    readonly_fields = ('id',)


admin.site.register(Meal, MealAdmin)
