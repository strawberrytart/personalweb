from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse

# Create your models here.

class Category(MPTTModel):

    Status = (
        ('True', 'True'),
        ('False', 'False'),
    )

    bool_choices = (
        (True, 'Yes'),
        (False, 'No'),
    )

    parent = TreeForeignKey('self',  blank = True, null = True, related_name = 'children', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=False)
    description = models.TextField()
    status = models.CharField(max_length=10, choices = Status)
    is_active = models.BooleanField(choices=bool_choices)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    image = models.ImageField(blank = True, upload_to = 'images/')

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        
        return reverse('category_detail', kwargs={'slug':self.slug})

    def get_all_products(self):

        # To display all products from categories and subcategories 
        category = self.get_descendants(include_self=True)
        return Product.objects.filter(category__in=category)

    
class Brand(models.Model):

    bool_choices = (
        (True, 'Yes'),
        (False, 'No'),
    )
    
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"

class Product(MPTTModel):

    Status = (
        ('True', 'True'),
        ('False', 'False'),
    )

    bool_choices = (
        (True, 'Yes'),
        (False, 'No'),
    )

    parent = TreeForeignKey('self',  blank = True, null = True, related_name = 'children', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product") #one to many relationship between Brand and Product class
    sku = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(blank = True, upload_to = 'images/')
    is_active = models.BooleanField(choices=bool_choices)
    is_featured = models.BooleanField(choices=bool_choices)
    is_bestseller = models.BooleanField(choices=bool_choices)
    quantity = models.IntegerField()
    description = RichTextUploadingField()
    status = models.CharField(max_length=10, choices = Status)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    category = TreeManyToManyField(Category, blank = True)

    class Meta:
        db_table = 'product'

    class MPTTMeta:
        order_insertion_by = ['name']


    def __str__(self):
        return f"{self.id}:{self.name}"

    
    def get_categories(self):
        return ",".join([str(p) for p in self.category.all()])

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{0}" style="width: 60px; height: 60px;" />'.format(self.image.url))
        else:
            return "No Image Found"
            
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        
        return reverse('category_detail', kwargs={'slug':self.slug})


class TechSpec(models.Model):

    attribute = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    product = models.ForeignKey(Product, on_delete= models.CASCADE, null=True, related_name='tech_spec')

    def __str__(self):
        
        return f"{self.attribute}: {self.value}"

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length = 50, blank= True)
    image = models.ImageField(blank= True, upload_to='images/')

    def __str__(self):
        return self.title
