from django.contrib import admin
from .models import Categorie, Customer, Order, Product
admin.site.register(Categorie)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)