from django import forms
from .models import Product
import bleach  

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image', 'category']

    def clean_description(self):
        description = self.cleaned_data.get('description')

        allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p', 'ul', 'li', 'ol', 'a']
        allowed_attrs = {'a': ['href', 'title']}

        cleaned_description = bleach.clean(description, tags=allowed_tags, attributes=allowed_attrs)

        return cleaned_description
