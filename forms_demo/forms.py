from django import forms
from .widgets import TagWidget

class CommaSeparatedTagsField(forms.Field):
    widget = TagWidget
    
    def to_python(self, value):
        """Converts the raw strings imput into a list of strings"""
        if not value:
            return []
        return [tag.strip() for tag in value.split(',')]
    
    def validate(self, value):
        """Runs after to_python, performs validation on the python list"""
        super().validate(value)
        if len(value) > 5:
            raise forms.ValidationError("You can onoy enter upto 5 tags")
        for tag in value:
            if ' ' in tag:
                raise forms.ValidationError("Tags cannot contain spaces")

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    tags = CommaSeparatedTagsField(required=False)