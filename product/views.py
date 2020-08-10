from django.shortcuts import render
from django.http import HttpResponse
from product.models import Category, Product, Images, Brand
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .filters import ProductFilter, BrandFilter
import json

# Create your views here.

def index(request):

    category = Category.objects.all()
    print(category)

    product_slider = Product.objects.all()
    product_latest = Product.objects.all().order_by('?') #random selected 4 products

    context = {'category': category, 'product_slider':product_slider, 'product_latest':product_latest}
    return render(request, 'home/index.html', context)

def product_detail(request,cat_id, cat_slug):

    category = Category.objects.get(pk=cat_id) # filter command will return a queryset
    print(category)
    product = Product.objects.all().filter(category=category) # find the products where the category is in the queryset 'category'

    return HttpResponse(product)

def product_page(request,id,slug):

    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context= {'product':product, 'images':images}
    return render(request, 'home/product_page.html', context)


def product(request):

    if request.GET:
        print('A query was passed in', request.GET)
        if request.GET.getlist('brand'):
            brand =request.GET.getlist('brand')
            print('Brand id is :',brand)
            products = Product.objects.all()
            brandFilter = BrandFilter(products = products, data= request.GET, queryset= products) #products filter the brands that belong to the products
            products = brandFilter.qs
            
        elif request.GET.get('category'):
            categories = request.GET.getlist('category')
            print('Category is:', categories)
            category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
            products = Product.objects.all()
            brandFilter = BrandFilter(category = category_0, data= request.GET, queryset= products) #products filter the brands that belong to the products
            products = brandFilter.qs
            brandFilter = BrandFilter(products = products, category = category_0, data= request.GET, queryset= products)#products filter the brands that belong to the products
            products = brandFilter.qs
        
        elif request.GET.get('page'):
            products = Product.objects.all()
            category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
            brandFilter = BrandFilter(products = products, category = category_0, data= request.GET, queryset= products) #products filter the brands that belong to the products



    else:
        print('Request is empty.')
        products = Product.objects.all()
        category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
        brandFilter = BrandFilter(products = products, category = category_0, data= request.GET, queryset= products) #products filter the brands that belong to the products
        products = brandFilter.qs

    category = Category.objects.all()
    #products = Product.objects.all()

    print("Request:", request.GET)



    print("Products:",products)

    paginator = Paginator(products,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'category': category, 'products': products,'brandFilter': brandFilter, 'page_obj': page_obj}
    return render(request, 'home/product.html', context)


def category(request, slug):
    category = Category.objects.all().filter(slug=slug)
    #print(category)
    category = category.get_descendants()
    products = Product.objects.filter(category__in = category)  
    #print('Request:',request.GET)
    brandFilter = BrandFilter(products = products, category = category, data= request.GET, queryset= products)
    context = {'category': category, 'products': products,'brandFilter': brandFilter}

    return render(request, 'home/category.html', context)
