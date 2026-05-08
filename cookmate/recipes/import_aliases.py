import json

from recipes.models import IngredientAlias

with open('dataset/ingredient_aliases.json') as file:

    data = json.load(file)

    for item in data:

        IngredientAlias.objects.get_or_create(
            alias=item['alias'].lower(),
            defaults={
                'normalized_name':
                item['normalized_name'].lower()
            }
        )

print("Ingredient Aliases Imported Successfully")