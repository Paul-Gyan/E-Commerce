from django.db import models
from users.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_categories')
    

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock_quantity = models.IntegerField()
    image_url = models.URLField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

class Promotion(models.Model):
    product = models.ForeignKey(Product, related_name='promotions', on_delete=models.CASCADE)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.discount_percentage}% off {self.product.name}"
    
    def is_valid(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')
    tracking_number = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        if hasattr(self.product, 'promotions') and self.product.promotions.exists():
            promotion = self.product.promotions.first()
            if promotion.is_valid():
                discount = self.product.price * (promotion.discount_percentage / 100)
                self.total_price = self.total_price * (1 - promotion.discount_percentage / 100)
        super(Order, self).save(*args, **kwargs)
        if self.status == 'Completed':
            self.product.stock_quantity -= self.quantity
            self.product.save()

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payments', on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, related_name='wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlisted_by', on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist {self.id} by {self.user.email}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.id} by {self.user.email}"

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, related_name='carts', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


    
    
