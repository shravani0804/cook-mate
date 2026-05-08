from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'signup/',
        views.signup,
        name='signup'
    ),

     path(
        'add-recipe/',
        views.add_recipe,
        name='add_recipe'
    ),

    path(
    'favorite/<int:recipe_id>/',
    views.toggle_favorite,
    name='toggle_favorite'
),

path(
    'clear-shopping-list/',
    views.clear_shopping_list,
    name='clear_shopping_list'
),

path(
    'favorites/',
    views.favorites,
    name='favorites'
),

path(
    'add-to-shopping/<int:recipe_id>/',
    views.add_to_shopping,
    name='add_to_shopping'
),
]