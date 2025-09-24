from django.shortcuts import render
from utils.recipes.factory import make_recipe


# Create your videf sobre_view(request):
def sobre_view(request):
    return render(request, 'cookbook/pages/sobre.html', context={'name': 'Brandão'})


def home_view(request):
    return render(request, 'cookbook/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
    })


def recipe_view(request, id):
    return render(request, 'cookbook/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })
