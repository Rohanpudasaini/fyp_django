from django.db import models
import datetime


# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'categories'

class Customer(models.Model):
    user_name = models.CharField(max_length=50, unique=True, default='None')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10) 
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Quote(models.Model):
    quote = models.CharField(max_length=200)
    author = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.author}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2, max_digits=8)
    category = models.ForeignKey(Categorie, on_delete= models.CASCADE, default=1)
    description = models.CharField(max_length=1050, blank=True, default='', null= True)
    image = models.ImageField(upload_to='uploads/products/')
    author = models.CharField(max_length=100, default='Traditional Stories')
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2, max_digits=8)
    created_at = models.DateTimeField(default=datetime.datetime.today)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default= '', blank= True)
    phone = models.CharField(max_length=20, default= '', blank= True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product
    


