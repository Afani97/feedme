from django.urls import path

from .views import profile, auth, home, meals

urlpatterns = [
    path('', home.home, name='home'),
    path('signup/', auth.signup_user, name='signup'),
    path('login/', auth.login_user, name='login'),
    path('logout/', auth.logout_user, name='logout'),
    path('profile/', profile.profile, name='profile'),
    path('profile/edit_cook/', profile.CookProfileForm.as_view(), name='edit_cook_profile'),
    path('profile/edit_eater/', profile.EaterProfileForm.as_view(), name='edit_eater_profile'),
    path('meals/new', meals.NewMealView.as_view(), name='new_meal'),
    path('meals/<uuid:meal_id>/favorite', meals.favorite_meal, name='favorite_meal'),
    path('meals/<uuid:meal_id>/view', meals.view_meal, name='view_meal'),
    path('meals/<uuid:meal_id>/start_cooking', meals.start_cooking_meal, name='start_meal'),
    path('meals/<pk>/update_status', meals.UpdateMealStatus.as_view(), name='update_meal_status'),
    path('meals/<pk>/update', meals.EditMealView.as_view(), name='edit_meal'),
    path('meals/<pk>/delete', meals.DeleteMealView.as_view(), name='delete_meal')
]