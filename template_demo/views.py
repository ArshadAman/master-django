from django.shortcuts import render
from django.contrib.auth.models import User

def template_test_view(request):
    # Create a dummy user for the example if one doesn't exist
    user, _ = User.objects.get_or_create(username = 'textuser', defaults={
        'first_name': 'Alice'
    })
    context = {'current_user':user}
    return render(request, 'template_demo/test.html', context)
