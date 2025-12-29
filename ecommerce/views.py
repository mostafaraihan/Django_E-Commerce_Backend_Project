import json
import random
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .auth_middleware import jwt_required
from .models import (Brand, Category, Product, ProductSlider, ProductDetail, User, ProductCart, ProductWish, Invoice,
                     InvoiceProduct)


def home(request):
    return render(request,'index.html')

# Before Login
def brand_list(request):
    data= list(Brand.objects.values("id","brandName","brandImg"))
    return JsonResponse({
        "status":True,
        "message":"success",
        "data":data
    })

def category_list(request):
    data = list(
        Category.objects.values("id", "categoryName", "categoryImg")
    )
    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })

def product_by_category(request, category_id):
    data = list(
        Product.objects.filter(category_id=category_id)
        .values(
            "id", "title", "price",
            "discount_price", "image", "remark", "star"
        )
    )
    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })

def product_by_remark(request, remark):
    data = list(
        Product.objects.filter(remark=remark)
        .values(
            "id", "title", "price",
            "discount_price", "image", "remark", "star"
        )
    )
    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })

def product_slider_list(request):
    data = list(
        ProductSlider.objects.values(
            "id", "title", "short_des", "price", "image"
        )
    )
    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })

@csrf_exempt
def product_by_keyword(request):
    keyword = request.GET.get("keyword", "")
    data = list(
        Product.objects.filter(
            title__icontains=keyword
        ).values(
            "id", "title", "price",
            "discount_price", "image", "remark"
        )
    )

    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })

def product_details(request, product_id):
    product = Product.objects.values(
        "id", "title", "price",
        "discount", "discount_price",
        "image", "remark", "star"
    ).get(id=product_id)

    details = ProductDetail.objects.values(
        "img1", "img2", "img3", "img4",
        "des", "color", "size"
    ).get(product_id=product_id)

    data = {
        "product": product,
        "details": details
    }
    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })

def product_by_brand(request, brand_id):
    data = list(
        Product.objects.filter(brand_id=brand_id)
        .values(
            "id", "title", "price",
            "discount_price", "image", "remark", "star"
        )
    )
    return JsonResponse({
        "status": True,
        "message": "success",
        "data": data
    })



# Login
@csrf_exempt
def user_login(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()

    if not email:
        return JsonResponse({"status": False, "message": "Email is required"})

    otp = str(random.randint(1000, 9999))

    user, created = User.objects.get_or_create(email=email, defaults={'otp': otp})
    if not created:
        user.otp = otp
        user.save()

    #Email

    return JsonResponse({"status": True, "message": f"{otp} OTP sent successfully"})



@csrf_exempt
def verify_otp(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    otp = data.get('otp', '').strip()

    if not email or not otp:
        return JsonResponse({"status": False, "message": "Email and OTP are required"})

    try:
        user = User.objects.get(email=email, otp=otp)
    except User.DoesNotExist:
        return JsonResponse({"status": False, "message": "Invalid email or OTP"})

    payload = {
        'user_id': user.id,
        'user_email': user.email,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'iat': datetime.now(timezone.utc)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return JsonResponse({
        "status": True,
        "message": "Login successful",
        "token": token,
        "data": {"user_id": user.id, "user_email": user.email}
    })


# After Login
@csrf_exempt
@jwt_required
def cart_add(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    color = data.get('color', '')
    size = data.get('size', '')
    qty = data.get('qty', '1')

    if not product_id:
        return JsonResponse({"status": False, "message": "Product ID is required"})

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"status": False, "message": "Product not found"})

    cart_item, created = ProductCart.objects.get_or_create(
        user_id=request.user_id,
        product_id=product_id,
        color=color,
        size=size,
        defaults={'qty': qty, 'price': product.discount_price}
    )

    if not created:
        cart_item.qty = str(int(cart_item.qty) + int(qty))
        cart_item.save()

    return JsonResponse({"status": True, "message": "Product added to cart"})


@csrf_exempt
@jwt_required
def cart_remove(request, cart_id):
    try:
        cart_item = ProductCart.objects.get(id=cart_id, user_id=request.user_id)
        cart_item.delete()
        return JsonResponse({"status": True, "message": "Product removed from cart"})
    except ProductCart.DoesNotExist:
        return JsonResponse({"status": False, "message": "Cart item not found"})


@jwt_required
def cart_list(request):
    cart_items = ProductCart.objects.filter(user_id=request.user_id).select_related('product')

    data = []
    for item in cart_items:
        data.append({
            "id": item.id,
            "product_id": item.product.id,
            "product_title": item.product.title,
            "product_image": item.product.image,
            "color": item.color,
            "size": item.size,
            "qty": item.qty,
            "price": item.price,
            "total": str(int(item.qty) * float(item.price))
        })

    return JsonResponse({"status": True, "message": "success", "data": data})


@csrf_exempt
@jwt_required
def wish_add(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')

    if not product_id:
        return JsonResponse({"status": False, "message": "Product ID is required"})

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"status": False, "message": "Product not found"})

    wish_item, created = ProductWish.objects.get_or_create(
        user_id=request.user_id,
        product_id=product_id
    )

    if not created:
        return JsonResponse({"status": False, "message": "Product already in wishlist"})

    return JsonResponse({"status": True, "message": "Product added to wishlist"})


@csrf_exempt
@jwt_required
def wish_remove(request, wish_id):
    try:
        wish_item = ProductWish.objects.get(id=wish_id, user_id=request.user_id)
        wish_item.delete()
        return JsonResponse({"status": True, "message": "Product removed from wishlist"})
    except ProductWish.DoesNotExist:
        return JsonResponse({"status": False, "message": "Wishlist item not found"})


@jwt_required
def wish_list(request):
    wish_items = ProductWish.objects.filter(user_id=request.user_id).select_related('product')

    data = []
    for item in wish_items:
        data.append({
            "id": item.id,
            "product_id": item.product.id,
            "product_title": item.product.title,
            "product_image": item.product.image,
            "product_price": item.product.price,
            "product_discount_price": item.product.discount_price,
            "product_star": item.product.star
        })

    return JsonResponse({"status": True, "message": "success", "data": data})


@csrf_exempt
@jwt_required
def create_invoice(request):
    data = json.loads(request.body)
    cus_details = data.get('cus_details', '')
    ship_details = data.get('ship_details', '')

    if not cus_details or not ship_details:
        return JsonResponse({"status": False, "message": "Customer and shipping details required"})

    cart_items = ProductCart.objects.filter(user_id=request.user_id)

    if not cart_items.exists():
        return JsonResponse({"status": False, "message": "Cart is empty"})

    total = 0
    for item in cart_items:
        total += int(item.qty) * float(item.price)

    vat = total * 0.05
    payable = total + vat

    tran_id = f"TXN{request.user_id}{datetime.now().strftime('%Y%m%d%H%M%S')}"

    invoice = Invoice.objects.create(
        user_id=request.user_id,
        total=str(total),
        vat=str(vat),
        payable=str(payable),
        cus_details=cus_details,
        ship_details=ship_details,
        tran_id=tran_id,
        val_id='',
        delivery_status='pending',
        payment_status='pending'
    )

    for item in cart_items:
        InvoiceProduct.objects.create(
            invoice_id=invoice.id,
            product_id=item.product_id,
            user_id=request.user_id,
            qty=item.qty,
            sale_price=item.price
        )

    cart_items.delete()

    return JsonResponse({
        "status": True,
        "message": "Invoice created successfully",
        "data": {
            "invoice_id": invoice.id,
            "tran_id": tran_id,
            "total": str(total),
            "vat": str(vat),
            "payable": str(payable)
        }
    })


@jwt_required
def invoice_list(request):
    invoices = Invoice.objects.filter(user_id=request.user_id).order_by('-created_at')

    data = []
    for invoice in invoices:
        invoice_products = InvoiceProduct.objects.filter(invoice_id=invoice.id).select_related('product')

        products = []
        for item in invoice_products:
            products.append({
                "product_id": item.product.id,
                "product_title": item.product.title,
                "product_image": item.product.image,
                "qty": item.qty,
                "sale_price": item.sale_price
            })

        data.append({
            "invoice_id": invoice.id,
            "tran_id": invoice.tran_id,
            "total": invoice.total,
            "vat": invoice.vat,
            "payable": invoice.payable,
            "cus_details": invoice.cus_details,
            "ship_details": invoice.ship_details,
            "delivery_status": invoice.delivery_status,
            "payment_status": invoice.payment_status,
            "created_at": invoice.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "products": products
        })

    return JsonResponse({"status": True, "message": "success", "data": data})
