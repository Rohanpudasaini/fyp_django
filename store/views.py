from django.shortcuts import redirect, render
from .models import Product, Quote
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User 
# from django.contrib.auth.forms import UserCreationForm
# from django import forms
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from store.recommend_main import recommend, df
import random
# Create your views here.

def home(request):
    products = Product.objects.all().order_by('-created_at')
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    sale_items = Product.objects.filter(is_sale=True).order_by('-created_at')[:1]
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
    # print(product.name)
    result = recommend(df,product.name.replace(":", ""))
    print(result)
    results = []
    if result:
        for items in result:
            item = Product.objects.filter(name__istartswith=items)
            if item:
                results.append(item)
    # print(results) 
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    return render(request,'product.html',{'product':product,'random_quotes':random_quotes,'recommended':results})

def recommended(request):
    result = recommend(df,"Harry Potter and the Prisoner of Azkaban Book 3")
    results = []
    # print(result)
    for i, items in enumerate(result):
        item = Product.objects.filter(name__istartswith=items)
        if item:
            results.append(item)
    # print(results)  
    quotes = Quote.objects.all()
    random_quotes = random.choice(quotes) if quotes.exists() else None
    return render(request, 'recommend.html',{'random_quotes':random_quotes, 'recommended':results})  

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')