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

    brand = django_filters.ModelMultipleChoiceFilter(queryset= Brand.objects.all(), widget=forms.CheckboxSelectMultiple)
    category = django_filters.ModelMultipleChoiceFilter(queryset= Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    
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