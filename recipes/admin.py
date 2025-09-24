from django.contrib import admin
from .models import Category, Recipe


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    ...  # Configuration for Category admin interface


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...  # Configuration for Recipe admin interface


admin.site.register(Category, CategoryAdmin)
# admin.site.register(Recipe, RecipeAdmin)  # Already registered using the decorator @admin.register