import os
import django
import pandas as pd
import random

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'cookmate.settings'
)

django.setup()

from recipes.models import (
    Recipe,
    Ingredient,
    Nutrition,
    Score
)

# LOAD CSV

df = pd.read_csv(
    'dataset/clean_recipes.csv'
)

for index, row in df.iterrows():

    try:

        recipe_name = str(
            row['name']
        ).strip()

        instructions = str(
            row['instructions']
        ).strip()

        ingredients_text = str(
            row['ingredients']
        ).lower()

        calories = float(
            row['calories']
        )

        protein = float(
            row['protein']
        )

        carbs = float(
            row['carbs']
        )

        fats = float(
            row['fats']
        )


        cooking_time = int(
            row['cooking_time']
        )

        difficulty = str(
            row['difficulty']
        ).strip()

        cuisine = str(
            row['cuisine']
        ).strip()

        # CREATE RECIPE

        recipe = Recipe.objects.create(

            name=recipe_name,

            instructions=instructions,

            cooking_time=cooking_time,

            difficulty=difficulty,

            cuisine=cuisine,

            popularity_score=random.randint(
                50,
                100
            )
        )

        # INGREDIENTS

        ingredient_list = ingredients_text.split(',')

        for ingredient_name in ingredient_list:

            ingredient_name = (
                ingredient_name.strip()
            )

            if ingredient_name:

                ingredient_obj, created = (
                    Ingredient.objects.get_or_create(
                        name=ingredient_name
                    )
                )

                recipe.ingredients.add(
                    ingredient_obj
                )

        # NUTRITION

        Nutrition.objects.create(

            recipe=recipe,

            calories=calories,

            protein=protein,

            carbs=carbs,

            fats=fats
        )

        # SCORE

        Score.objects.create(

            recipe=recipe,

            match_score=0,

            health_score=0,

            ease_score=0,

            final_score=0,

            popularity_score=recipe.popularity_score
        )

        print(
            f"Imported: {recipe.name}"
        )

    except Exception as e:

        print(
            f"Error in row {index}: {e}"
        )

print(
    "DATASET IMPORT COMPLETED"
)