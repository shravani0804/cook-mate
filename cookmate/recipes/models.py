from django.db import models
from django.contrib.auth.models import User

# Ingredient Model
class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Recipe Model
class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.ManyToManyField(Ingredient)
    instructions = models.TextField()
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    image = models.ImageField(upload_to='recipe_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    popularity_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


# Nutrition Model
class Nutrition(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()


# Score Model
class Score(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE)
    match_score = models.FloatField()
    health_score = models.FloatField()
    ease_score = models.FloatField()
    final_score = models.FloatField()
    popularity_score = models.IntegerField(default=0)


# Shopping List Model
class ShoppingList(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.ingredient.name}"

class SearchHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    ingredients = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True) 

    searched_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.ingredients}"

class IngredientAlias(models.Model):
    alias = models.CharField(max_length=100, unique=True)
    normalized_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.alias} → {self.normalized_name}"    
    
class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.recipe.name}"