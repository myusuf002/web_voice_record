from django.shortcuts import render

# Create your views here.

def viewIndex(request):  
    context = {
        'title': "Listen",
        'page': "listen"    }
    return render(request, 'listen/index.html', context)

