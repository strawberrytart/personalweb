from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Brand, Images, TechSpec
from mptt.admin import DraggableMPTTAdmin
# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
     list_display = ('name','parent', 'created_at', 'is_active')
     list_filter = ('is_active',)

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5
    readonly_fields = ('image_tag',)

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 45px; height:45px;" />'.format(obj.image.url))

class ProductTechSpecInline(admin.TabularInline):
    model = TechSpec
    extra = 5
    
class DraggableCategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','brand','created_at', 'get_categories','image_tag')
    readonly_fields = ('image_tag',)
    inlines = [
        ProductImageInline,
        ProductTechSpecInline,
    ]

    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category,DraggableCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Images)
admin.site.register(TechSpec)