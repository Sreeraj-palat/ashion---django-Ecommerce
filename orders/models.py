from django.db import models
from accounts.models import Account
from store.models import Product, Variation



class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100 ,null=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100) # this is the total amount paid
    paid = models.BooleanField(default=False)   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Ordered', 'Ordered'),
        ('shipped', 'shipped'),
        ('out_for_delivery', 'out_for_delivery'),
        ('delivered','delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    def __str__(self):
        return self.order_number



class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name



class Delivery_address(models.Model):
    user            = models.ForeignKey(Account, on_delete=models.SET_NULL,null=True)
    firstname       = models.CharField(max_length=50,null=False)
    lastname        = models.CharField(max_length=50,null=True)
    addressfield_1  = models.CharField(max_length=250,null=False)
    addressfield_2  = models.CharField(max_length=50,null=True)
    city            = models.CharField(max_length=50,null=False)
    state           = models.CharField(max_length=50,null=False)
    country         = models.CharField(max_length=50,null=False)
    post_code       = models.CharField(max_length=50,null=False)
    phonenumber     = models.CharField(max_length=50,null=False)
    email           = models.EmailField(max_length=50,null=False)
    
    objects = models.Manager()
    
    def __str__(self):
        return self.user.username
            