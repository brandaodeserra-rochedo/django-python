from django.shortcuts import render, get_object_or_404, get_list_or_404
from recipes.models import Recipe


# Create your videf sobre_view(request):
def sobre_view(request):
    return render(request, 'recipes/pages/sobre.html',
                  context={'name': 'Brandão'})


def home(request):
    recipes = Recipe.objects.filter(
            is_published=True,
        ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - Category | '
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })
