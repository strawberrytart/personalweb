import django_filters
from product.models import Product, Category, Brand
from django.db import models
from django import forms

class ProductFilter(django_filters.FilterSet): #inherit from django_filters.FilterSet
    
    #field_name refers to the model field to filter on.
    name = django_filters.CharFilter(lookup_expr='icontains', field_name='name')

    class Meta:
        model = Category #building filter for Category model
        fields = ('name',)
        

class BrandFilter(django_filters.FilterSet):

    brand = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple)
    category = django_filters.ModelMultipleChoiceFilter(widget=forms.CheckboxSelectMultiple)
    

    #order_by_field = 'ordering'
    ordering = django_filters.OrderingFilter(

        choices = (
            ('-is_featured', 'Featured'),
            ('-created_at', 'Date, New to Old'),
            ('created_at', 'Date, Old to New' ),
        ),
        fields = (
            ('is_featured', 'featured'), #{model field name, parameter in the URL}
            ('created_at', 'created'),
            ('price', 'price'),
        ),
        field_labels = {
            'is_featured': 'Featured', #{model field name, human readable label}
            'created_at': 'Date',
            'price': 'Price',
        }
    )

    class Meta:
        model = Product 
        fields = ('brand','category') 

    
    def __init__(self, products= "", category=Category.objects.none(),*args, **kwargs):

        #super(BrandFilter, self).__init__(*args, **kwargs)
        #self.filters['brand'].queryset = Brand.objects.filter(product__in=products).distinct()  
        
        #self.filters['category'].queryset = category

        super(BrandFilter, self).__init__(*args, **kwargs)
        self.filters['brand'].queryset = Brand.objects.filter(product__in=products).distinct()  
        self.filters['category'].queryset = category
    
#Brand.objects.filter(product__in=c.product_set.all())
#Brand.objects.filter(product__category__name='Pumps')
#Brand.objects.filter(product__category__in=c).distinct()