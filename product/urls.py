from django.urls import path
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name= 'index'),
    path("category/<int:cat_id>/<str:cat_slug>", views.product_detail, name= 'product_detail'),
    path("product/<int:id>/<slug:slug>",views.product_page, name='product_page'),
    path("product/", views.product, name='product'),
    path("<str:slug>/", views.category, name='category'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)