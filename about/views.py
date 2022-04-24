from django.shortcuts import render


# Create your views here.

def contact(request):
    return render(request, 'about/contact.html')


def suggestions(request):
    return render(request, 'about/suggestions.html')
