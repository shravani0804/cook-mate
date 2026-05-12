import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "cookmate.settings"
)

django.setup()

from recipes.models import Recipe

recipes = Recipe.objects.all()

seen = set()

deleted_count = 0

for recipe in recipes:

    # remove Type and Variation parts
    base_name = recipe.name.split("Type")[0].strip()

    if base_name.lower() in seen:

        recipe.delete()

        deleted_count += 1

    else:

        seen.add(base_name.lower())

print(f"Deleted {deleted_count} duplicate recipes")