from django.shortcuts import render


# Create your videf sobre_view(request):
def sobre_view(request):
    return render(request, 'cookbook/sobre.html', context={'name': 'Alexandre Brandão'})


def index_view(request):
    return render(request, 'global/index.html')
