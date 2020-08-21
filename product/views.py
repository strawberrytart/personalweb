from django.shortcuts import render
from django.http import HttpResponse
from product.models import Category, Product, Images, Brand
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .filters import ProductFilter, BrandFilter
from django.core.exceptions import ObjectDoesNotExist
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
    previous_url = request.META.get('HTTP_REFERER').split('/')[-2]
    try: 
        category = Category.objects.get(slug = previous_url)
        category = category.get_ancestors(include_self= True)
    except ObjectDoesNotExist:
        category = None
    print("Previous URL", previous_url)
    print("Category:", category)
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context= {'product':product, 'images':images, 'category': category}
    return render(request, 'home/product_page.html', context)


def product(request):
    if request.GET: # request.GET contains query filter
        n = len(request.GET)
        print(n)
        if n>1:
            if request.GET.get('brand'):
                # query contains "brand"
                print("brand, page and category")
                #products = Product.objects.all()
                category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
                brandFilter = BrandFilter(category = category_0,data= request.GET) #filter products based on category
                products = brandFilter.qs
                print("brandfilter.qs returns:", products)
                brand_list=[]
                #create a list of brands associated with the products 
                for p in  products:
                    brand_id = p.brand.id
                    if brand_id not in brand_list: #prevent duplicates in the list
                        brand_list.append(brand_id)

                print("A_list:", brand_list)

                brand_query_filter = request.GET.getlist('brand') #grab the brand queries from url

                print("brand:", brand_query_filter)

                matched = []
                # creates a list of brands that match the "brand" query from url from brand_list
                for i in brand_query_filter: 
                    if int(i) in brand_list:
                        matched.append(i)

                print("matched:",matched)
                # QueryDict is not mutable. Create a copy to make it mutable. 
                querydict = request.GET.copy()
                print("Before pop:", querydict)
                querydict.pop('brand')
                print("After pop:", querydict)
                for i in matched:
                    querydict.update({'brand': i})
                print(querydict.getlist('brand'))
                brandFilter = BrandFilter(products = products, category = category_0, data= querydict, queryset= products) #products filter the brands that belong to the products
            
            else:  #"brand" not in query, only "category" and "page"
                print("only category and page")
                category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
                products = Product.objects.all()
                brandFilter = BrandFilter(category = category_0, data= request.GET) #filter products based on the category query
                products = brandFilter.qs
                print("brand.qs:",products)
                brandFilter = BrandFilter(products = products, category = category_0, data= request.GET)#filter products based on category and render brands associated with that category                print("second:", brandFilter.qs)
        
        else: # query only contains either category or brand, not both
            if request.GET.getlist('brand'):
                products = Product.objects.all()
                category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
                brandFilter = BrandFilter(products = products, data= request.GET) # filter product based on the brand query
                products = brandFilter.qs 
                
            elif request.GET.get('category'):
                category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
                products = Product.objects.all()
                brandFilter = BrandFilter(category = category_0, data= request.GET) #filter products based on the category query
                products = brandFilter.qs
                print("brand.qs:",products)
                brandFilter = BrandFilter(products = products, category = category_0, data= request.GET)#filter products based on category and render brands associated with that category                print("second:", brandFilter.qs)
   
            elif request.GET.get('page'):
                print("Page turnt.")
                products = Product.objects.all()
                category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
                brandFilter = BrandFilter(products = products, category = category_0, data= request.GET, queryset= products) #products filter the brands that belong to the products
            else:
                print(request.GET)
                print("Only ordering was passed in")
                products = Product.objects.all()
                category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
                brandFilter = BrandFilter(products = products, category = category_0, data= request.GET, queryset= products) #products filter the brands that belong to the products
                products = brandFilter.qs 

    else:
        # request.GET is empty, no query sent. 
        products = Product.objects.all()
        category_0 = Category.objects.filter(level=0) # Grab all categories at node level 0 
        brandFilter = BrandFilter(products = products, category = category_0, data= request.GET) #products filter the brands that belong to the products

    category = Category.objects.all()
    paginator = Paginator(products,5) #show 5 products on 1 page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'category': category, 'products': products,'brandFilter': brandFilter, 'page_obj': page_obj}
    return render(request, 'home/product.html', context)


def category(request, slug):
    cat = Category.objects.all().filter(slug=slug)
    products = Product.objects.filter(category__in = cat)
    category = cat.get_descendants()
    print("Descendants:" ,category)
    #print('Request:',request.GET)
    brandFilter = BrandFilter(products = products, category = category, data= request.GET, queryset= products)
    products = brandFilter.qs
    print(products)
    paginator = Paginator(products, 2) # show 3 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'category': category, 'products': products,'brandFilter': brandFilter, 'page_obj': page_obj, 'cat': cat}

    return render(request, 'home/category.html', context)

def show_category(request,hierarchy= None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()

    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug = slug)

    try:
        instance = Category.objects.get(parent=parent,slug=category_slug[-1])
    except:
        instance = get_object_or_404(Post, slug = category_slug[-1])
        return render(request, "postDetail.html", {'instance':instance})
    else:
        return render(request, 'categories.html', {'instance':instance})