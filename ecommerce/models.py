from django.db import models

class Brand(models.Model):
    brandName = models.CharField(max_length=255)
    brandImg = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    categoryName = models.CharField(max_length=255)
    categoryImg = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    REMARK_CHOICES = [
        ('popular', 'Popular'),
        ('new', 'New'),
        ('top', 'Top'),
        ('special', 'Special'),
    ]
    title = models.CharField(max_length=255)
    short_des = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    discount = models.PositiveSmallIntegerField()
    discount_price = models.CharField(max_length=50)
    image = models.CharField(max_length=255)
    stock = models.PositiveSmallIntegerField()
    star = models.FloatField()
    remark = models.CharField(max_length=20, choices=REMARK_CHOICES)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductSlider(models.Model):
    title = models.CharField(max_length=255)
    short_des = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    image = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductDetail(models.Model):
    img1 = models.CharField(max_length=255)
    img2 = models.CharField(max_length=255)
    img3 = models.CharField(max_length=255)
    img4 = models.CharField(max_length=255)
    des = models.TextField()
    color = models.CharField(max_length=255)
    size = models.CharField(max_length=255)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomerProfile(models.Model):
    cus_name = models.CharField(max_length=255)
    cus_add = models.CharField(max_length=255)
    cus_city = models.CharField(max_length=255)
    cus_state = models.CharField(max_length=255)
    cus_postcode = models.CharField(max_length=255)
    cus_country = models.CharField(max_length=255)
    cus_phone = models.CharField(max_length=255)
    cus_fax = models.CharField(max_length=255)

    ship_name = models.CharField(max_length=255)
    ship_add = models.CharField(max_length=255)
    ship_city = models.CharField(max_length=255)
    ship_state = models.CharField(max_length=255)
    ship_postcode = models.CharField(max_length=255)
    ship_country = models.CharField(max_length=255)
    ship_phone = models.CharField(max_length=255)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    color = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    qty = models.CharField(max_length=50)
    price = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductReview(models.Model):
    description = models.CharField(max_length=255)
    rating = models.CharField(max_length=50)

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductWish(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Invoice(models.Model):
    DELIVERY_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
    ]

    total = models.CharField(max_length=50)
    vat = models.CharField(max_length=50)
    payable = models.CharField(max_length=50)

    cus_details = models.CharField(max_length=255)
    ship_details = models.CharField(max_length=255)

    tran_id = models.CharField(max_length=255)
    val_id = models.CharField(max_length=255)

    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS)
    payment_status = models.CharField(max_length=50)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    qty = models.CharField(max_length=50)
    sale_price = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SSLCommerzAccount(models.Model):
    store_id = models.CharField(max_length=255)
    store_passwd = models.CharField(max_length=255)
    currency = models.CharField(max_length=50)

    success_url = models.CharField(max_length=255)
    fail_url = models.CharField(max_length=255)
    cancel_url = models.CharField(max_length=255)
    ipn_url = models.CharField(max_length=255)
    init_url = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Policy(models.Model):
    POLICY_TYPES = [
        ('about', 'About'),
        ('refund', 'Refund'),
        ('privacy', 'Privacy'),
        ('terms', 'Terms'),
    ]
    type = models.CharField(max_length=20, choices=POLICY_TYPES)
    des = models.TextField()