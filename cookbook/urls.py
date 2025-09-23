from django.urls import path 
from cookbook.views import sobre_view, index_view


urlpatterns = [
    path('sobre/', sobre_view),
    path('', index_view),
]