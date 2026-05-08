import os
import django
import pandas as pd
import ast
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
    'dataset/foods_data.csv'
)

for index, row in df.iterrows():

    try:

        recipe_name = str(row['name'])

        summary = str(row['summary'])

        ingredients_raw = row['ingredients']

        nutrition_raw = row['nutritions']

        times_raw = row['Times']

        # COOKING TIME
        cooking_time = 30

        if 'CookTime' in str(times_raw):

            import re

            match = re.search(
                r"CookTime':\s*'(\d+)",
                str(times_raw)
            )

            if match:
                cooking_time = int(match.group(1))

        # CREATE RECIPE
        recipe = Recipe.objects.create(
            name=recipe_name,
            instructions=summary,
            cooking_time=cooking_time,
            difficulty=random.choice([
                'Easy',
                'Medium',
                'Hard'
            ]),
            popularity_score=random.randint(50, 100)
        )

        # INGREDIENTS
        ingredients_list = ast.literal_eval(
            ingredients_raw
        )

        for ingredient_name in ingredients_list:

            ingredient_obj, created = Ingredient.objects.get_or_create(
                name=ingredient_name.lower().strip()
            )

            recipe.ingredients.add(
                ingredient_obj
            )

        # NUTRITION VALUES
        calories = 0
        protein = 0
        carbs = 0
        fats = 0

        nutrition_text = str(nutrition_raw)

        import re

        calorie_match = re.search(
            r"Calories':\s*'(\d+)",
            nutrition_text
        )

        protein_match = re.search(
            r"Protein':\s*'(\d+)",
            nutrition_text
        )

        carb_match = re.search(
            r"Carbohydrates':\s*'(\d+)",
            nutrition_text
        )

        fat_match = re.search(
            r"Fat':\s*'(\d+)",
            nutrition_text
        )

        if calorie_match:
            calories = float(calorie_match.group(1))

        if protein_match:
            protein = float(protein_match.group(1))

        if carb_match:
            carbs = float(carb_match.group(1))

        if fat_match:
            fats = float(fat_match.group(1))

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
            health_score=random.uniform(5, 10),
            ease_score=random.uniform(5, 10),
            final_score=random.uniform(5, 10),
            popularity_score=recipe.popularity_score
        )

        print(f"Imported: {recipe_name}")

    except Exception as e:

        print(f"Error in row {index}: {e}")

print("DATA IMPORT COMPLETED")