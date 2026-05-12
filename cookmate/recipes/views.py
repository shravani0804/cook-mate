from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import (
    Recipe,
    Ingredient,
    Nutrition,
    SearchHistory,
    ShoppingList,
    Favorite,
    IngredientAlias
)


# SIGNUP

def signup(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('/home/')

    else:

        form = UserCreationForm()

    return render(
        request,
        'registration/signup.html',
        {
            'form': form
        }
    )


# ROLE REDIRECT

def role_redirect(request):

    if request.user.is_superuser:

        return redirect('/admin-dashboard/')

    return redirect('/landing/')


# LANDING PAGE

@login_required
def landing_page(request):

    trending_recipes = Recipe.objects.all()[:12]

    return render(

        request,

        'landing.html',

        {

            'trending_recipes': trending_recipes

        }
    )


# HOME / RECOMMENDATION PAGE

def home(request):

    if not request.user.is_authenticated:

        return redirect('/accounts/login/')

    recommended_recipes = []

    recent_searches = []

    shopping_list = []

    favorite_recipe_ids = []

    trending_recipes = Recipe.objects.order_by(
        '-id'
    )[:6]

    # USER DATA

    favorite_recipe_ids = Favorite.objects.filter(
        user=request.user
    ).values_list(
        'recipe_id',
        flat=True
    )

    recent_searches = SearchHistory.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    shopping_list = ShoppingList.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # FORM SUBMIT

    if request.method == 'POST':

        user_input = request.POST.get(
            'ingredients',
            ''
        )

        selected_goal = request.POST.get(
            'health_goal'
        )

        # SAVE SEARCH HISTORY

        if user_input:

            SearchHistory.objects.create(

                user=request.user,

                ingredients=user_input
            )

        # USER INGREDIENTS

        user_ingredients = [

            item.strip().lower()

            for item in user_input.split(',')

            if item.strip()
        ]

        # NORMALIZE INGREDIENTS

        normalized_ingredients = []

        for ingredient in user_ingredients:

            alias = IngredientAlias.objects.filter(
                alias=ingredient
            ).first()

            if alias:

                normalized_ingredients.append(
                    alias.normalized_name.lower()
                )

            else:

                normalized_ingredients.append(
                    ingredient.lower()
                )

        recipes = Recipe.objects.all()

        all_missing = []

        for recipe in recipes:

            recipe_ingredients = [

                ingredient.name.lower()

                for ingredient in recipe.ingredients.all()
            ]

            matched = []

            missing = []

            for ingredient in recipe_ingredients:

                if ingredient in normalized_ingredients:

                    matched.append(ingredient)

                else:

                    missing.append(ingredient)

            # ONLY MATCHED RECIPES

            if matched:

                # MATCH SCORE

                match_score = (

                    len(matched) /

                    len(recipe_ingredients)

                ) * 100

                # HEALTH SCORE

                health_score = 50

                if hasattr(recipe, 'nutrition'):

                    if (

                        selected_goal == 'weight_loss'

                        and recipe.nutrition.calories < 400

                    ):

                        health_score = 90

                    elif (

                        selected_goal == 'muscle_gain'

                        and recipe.nutrition.protein > 15

                    ):

                        health_score = 90

                # EASE SCORE

                ease_score = max(
                    0,
                    100 - (len(missing) * 10)
                )

                # FINAL SCORE

                final_score = (

                    (match_score * 0.5)

                    +

                    (health_score * 0.3)

                    +

                    (ease_score * 0.2)

                )

                recommended_recipes.append({

                    'recipe': recipe,

                    'matched': matched,

                    'missing': missing,

                    'match_score': round(
                        match_score,
                        1
                    ),

                    'health_score': round(
                        health_score,
                        1
                    ),

                    'ease_score': round(
                        ease_score,
                        1
                    ),

                    'final_score': round(
                        final_score,
                        1
                    )
                })

                all_missing.extend(missing)

        # SORT

        recommended_recipes = sorted(

            recommended_recipes,

            key=lambda x: x['final_score'],

            reverse=True
        )

        # TOP 10

        recommended_recipes = recommended_recipes[:10]

        # UNIQUE MISSING

        unique_missing = list(set(all_missing))

        # SHOPPING LIST

        for ingredient_name in unique_missing:

            ingredient_obj = Ingredient.objects.filter(
                name__iexact=ingredient_name
            ).first()

            if ingredient_obj:

                exists = ShoppingList.objects.filter(

                    user=request.user,

                    ingredient=ingredient_obj

                ).exists()

                if not exists:

                    ShoppingList.objects.create(

                        user=request.user,

                        ingredient=ingredient_obj
                    )

        # RELOAD SHOPPING LIST

        shopping_list = ShoppingList.objects.filter(
            user=request.user
        ).order_by('-created_at')

    return render(

        request,

        'home.html',

        {

            'recipes': recommended_recipes,

            'recent_searches': recent_searches,

            'shopping_list': shopping_list,

            'favorite_recipe_ids': favorite_recipe_ids,

            'trending_recipes': trending_recipes
        }
    )


# FAVORITES

@login_required
def toggle_favorite(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    favorite = Favorite.objects.filter(

        user=request.user,

        recipe=recipe
    )

    if favorite.exists():

        favorite.delete()

    else:

        Favorite.objects.create(

            user=request.user,

            recipe=recipe
        )

    return redirect('/home/')


# FAVORITES PAGE

@login_required
def favorites(request):

    favorite_items = Favorite.objects.filter(
        user=request.user
    ).select_related('recipe')

    return render(

        request,

        'favorites.html',

        {

            'favorite_items': favorite_items

        }
    )


# SHOPPING LIST

@login_required
def clear_shopping_list(request):

    ShoppingList.objects.filter(
        user=request.user
    ).delete()

    return redirect('/home/')


@login_required
def add_to_shopping(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    user_ingredients = []

    latest_search = SearchHistory.objects.filter(
        user=request.user
    ).order_by('-created_at').first()

    if latest_search:

        user_ingredients = [

            ingredient.strip().lower()

            for ingredient in latest_search.ingredients.split(',')
        ]

    recipe_ingredients = recipe.ingredients.all()

    for ingredient in recipe_ingredients:

        if ingredient.name.lower() not in user_ingredients:

            exists = ShoppingList.objects.filter(

                user=request.user,

                ingredient=ingredient
            ).exists()

            if not exists:

                ShoppingList.objects.create(

                    user=request.user,

                    ingredient=ingredient
                )

    return redirect('/home/')


# ADD RECIPE

@login_required
@login_required
def add_recipe(request):

    if request.method == "POST":

        # BASIC DATA

        name = request.POST.get("name")

        instructions = request.POST.get("instructions")

        cooking_time = request.POST.get("cooking_time")

        difficulty = request.POST.get("difficulty")

        cuisine = request.POST.get("cuisine")

        image = request.FILES.get("image")

        ingredients_text = request.POST.get("ingredients")

        # CREATE RECIPE

        recipe = Recipe.objects.create(

            name=name,

            instructions=instructions,

            cooking_time=cooking_time,

            difficulty=difficulty,

            cuisine=cuisine,

            image=image,

            user=request.user
        )

        # INGREDIENTS

        ingredients_list = ingredients_text.split(",")

        for ingredient_name in ingredients_list:

            ingredient_name = ingredient_name.strip().lower()

            ingredient, created = Ingredient.objects.get_or_create(

                name=ingredient_name
            )

            recipe.ingredients.add(ingredient)

        # NUTRITION

        calories = request.POST.get("calories")

        protein = request.POST.get("protein")

        carbs = request.POST.get("carbs")

        fats = request.POST.get("fats")

        if calories and protein and carbs and fats:

            Nutrition.objects.create(

                recipe=recipe,

                calories=calories,

                protein=protein,

                carbs=carbs,

                fats=fats
            )

        return redirect("/landing/")

    return render(request, "add_recipe.html")
    


# RECIPE DETAIL

def recipe_detail(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id
    )

    nutrition = Nutrition.objects.filter(
        recipe=recipe
    ).first()

    return render(

        request,

        'recipe_detail.html',

        {

            'recipe': recipe,

            'nutrition': nutrition
        }
    )


# ADMIN DASHBOARD

@login_required
def admin_dashboard(request):

    total_recipes = Recipe.objects.count()

    total_users = User.objects.count()

    total_favorites = Favorite.objects.count()

    total_ingredients = Ingredient.objects.count()

    latest_recipes = Recipe.objects.order_by('-id')[:5]

    context = {

        'total_recipes': total_recipes,

        'total_users': total_users,

        'total_favorites': total_favorites,

        'total_ingredients': total_ingredients,

        'latest_recipes': latest_recipes,
    }

    return render(

        request,

        'admin_dashboard.html',

        context
    )