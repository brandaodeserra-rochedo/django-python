from django.urls import path
from recipes.views import sobre_view, home, recipe, category, search

app_name = 'recipes'

urlpatterns = [
    path('sobre/', sobre_view, name='sobre'),
    path('', home, name='home'),
    path('recipes/<int:id>/', recipe, name='recipe'),
    path('recipes/category/<int:category_id>/', category, name="category"),
    path('recipes/search/', search, name='search'),
]
