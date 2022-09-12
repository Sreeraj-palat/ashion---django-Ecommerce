from django.contrib import admin
from .models import Product, Variation,ReviewRating
from image_cropping import ImageCroppingMixin

# Register your models here.

class ProductAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug' : ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active') 
    list_editable = ('is_active',)   


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
