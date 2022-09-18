from dataclasses import fields
from pyexpat import model
from django import forms
from store.models import Product, Variation
from category.models import Category
from coupons.models import Coupons




class productForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description', 'price', 'stock', 'images', 'image_1', 'image_2', 'image_3', 'image_4', 'category']

        

    def __init__(self, *args, **kwargs):
        super(productForm,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control' 





class CategoryForm(forms.ModelForm):
    class Meta :
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CategoryForm,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control' 


class VariationForm(forms.ModelForm):
    class Meta :
        model = Variation
        fields = ['product', 'variation_category', 'variation_value']


    def __init__(self, *args, **kwargs):
        super(VariationForm,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control'    



class AddCouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(AddCouponForm,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control'     