from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def indexPageView(request):
    
    context = {}

    return render(request, 'portfolioApp/index.html', context)
