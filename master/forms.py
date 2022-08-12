from django import forms
from store.models import Product




class productForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'slug', 'description', 'price', 'stock', 'images', 'image_1', 'image_2', 'image_3', 'image_4', 'category']

        

    def __init__(self, *args, **kwargs):
        super(productForm,self).__init__(*args,**kwargs)        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] =  'form-control'  
    