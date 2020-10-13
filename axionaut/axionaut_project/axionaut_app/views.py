from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def commandes(request):
    return render(request, 'axionaut_app/commandes.html', {})