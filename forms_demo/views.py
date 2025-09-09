# forms_demo/views.py
from django.shortcuts import render
from .forms import ProductForm

def product_form_view(request):
    if request.method == 'POST':
        print("Raw POST data:", request.POST) # <-- Add this line
        form = ProductForm(request.POST)
        if form.is_valid():
            print("Form is valid!")
            print("Cleaned data:", form.cleaned_data)
    else:
        form = ProductForm()
    return render(request, 'forms_demo/product_form.html', {'form': form})