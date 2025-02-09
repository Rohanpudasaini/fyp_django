from django.contrib import admin
from .models import Categorie, Customer, Order, Product, Profile
from django.contrib.auth.models import User
admin.site.register(Categorie)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Profile)

class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name","email"]
    inlines = [ProfileInLine]
    
admin.site.unregister(User)

admin.site.register(User, UserAdmin)