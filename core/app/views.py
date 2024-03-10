from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')
    
def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'services.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def designs(request):
    return render(request, 'designs.html')


