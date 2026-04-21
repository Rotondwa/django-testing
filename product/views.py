from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm

# Create your views here.
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
