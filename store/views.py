from django.shortcuts import redirect, render
from .models import Product, Quote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages
from .forms import SignUpForm
import random
# Create your views here.

def home(request):
    products = Product.objects.all().order_by('-created_at')
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    sale_items = Product.objects.filter(is_sale=True).order_by('-created_at')[:3]
    return render(request, 'home.html',{'products':products,'sale_items':sale_items,'random_quotes':random_quotes})

def about(request):
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    return render(request, 'about.html',{'random_quotes':random_quotes})

def login_user(request):
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Sucessfull, Welcome to Book Town")
            return redirect('home')
        else:
            messages.warning(request, "Invalide login details")
            return render(request, 'login.html', {'random_quotes':random_quotes})
    else:
        return render(request, 'login.html', {'random_quotes':random_quotes})
    


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out...Thank you"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username= username, password = password)
            login(request,user)
            messages.success(request, "Registration Sucessfull, Welcome to Book Town")
            return redirect('home')
        else:
            messages.warning(request, "The User already exsist or your password is very similar to username")
            return redirect('register')
    else:
        quotes = Quote.objects.all()
        random_quotes = random.choice(quotes) if quotes.exists() else None
        return render(request, 'register.html',{'random_quotes':random_quotes,'form':form})
    
def product(request,pk):
    product = Product.objects.get(id=pk)
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    return render(request,'product.html',{'product':product,'random_quotes':random_quotes})