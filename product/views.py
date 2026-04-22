from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
import requests
from requests.exceptions import RequestException
from django.http import JsonResponse, HttpResponse


# Create your views here.
def post(request):
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts/1')
        # retutns an error if any error occurers when we are fetching data
        response.raise_for_status()
        return JsonResponse(response.json())
    except RequestException as e:
        # Log the error in a real application

        # Return a 503 Service Unavailable response
        return HttpResponse('Service Unavailable', status=503)

@login_required
def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

def homepage(request):
    return render(request, 'index.html')

def products(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
        else:
            print(form.errors)
            context = {
                'products': Product.objects.all(),
                'form': form
            }
            return render(request, 'products.html', context)

    products = Product.objects.all()
    context = {
        'products': products,
        'form': ProductForm()
    }
    return render(request, 'products.html', context)
