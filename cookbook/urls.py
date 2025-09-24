from django.urls import path 
from cookbook.views import sobre_view, home_view, recipe_view

app_name = 'recipes'

urlpatterns = [
    path('sobre/', sobre_view, name='sobre'),
    path('', home_view, name='home'),
    path('recipes/<int:id>/', recipe_view, name='recipe'),
]