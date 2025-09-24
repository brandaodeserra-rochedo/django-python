from django.shortcuts import render, get_object_or_404,get_list_or_404
from .models import Recipe
from cookbook.models import Recipe
from django.http import Http404


# Create your videf sobre_view(request):
def sobre_view(request):
    return render(request, 'cookbook/pages/sobre.html', context={'name': 'Brandão'})


def home_view(request):
    recipes = Recipe.objects.filter(
            is_published=True,
        ).order_by('-id')
    
    return render(request, 'cookbook/pages/home.html', context={
        'recipes': recipes,
    })


def category_view(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    return render(request, 'cookbook/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe_view(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'cookbook/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
