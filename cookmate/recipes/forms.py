from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe

        fields = [
            'name',
            'instructions',
            'cooking_time',
            'difficulty',
            'image'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control'
            }),

            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'difficulty': forms.Select(
                choices=[
                    ('easy', 'Easy'),
                    ('medium', 'Medium'),
                    ('hard', 'Hard')
                ],
                attrs={
                    'class': 'form-control'
                }
            )
        }