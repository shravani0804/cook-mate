from django.contrib import admin
from .models import (
    Recipe,
    Ingredient,
    Nutrition,
    Score,
    ShoppingList,
    SearchHistory,
    IngredientAlias
)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('ingredients',)


admin.site.register(Ingredient)
admin.site.register(Nutrition)
admin.site.register(Score)
admin.site.register(ShoppingList)
admin.site.register(IngredientAlias)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ingredients', 'created_at')
    ordering = ('-created_at',)