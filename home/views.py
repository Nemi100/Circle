from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view to return the index page """
    
    return render(request, 'home/index.html')


def learn_more(request):
    return render(request, 'home/learn_more.html')