from datetime import timezone

import jwt
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
import json,random,string

from Django_E_Commerce_Backend_Project import settings
from .models import (
    Brand,
    Category,
    Product,
    ProductSlider,
    ProductDetail,
    User,
)


# -------------------- HOME --------------------
def index(request):
    return render(request, 'index.html')


# -------------------- BRAND --------------------
def brand_list(request):
    data = list(
        Brand.objects.values(
            'id', 'brandName', 'brandImg'
        )
    )
    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })


# -------------------- CATEGORY --------------------
def category_list(request):
    data = list(
        Category.objects.values(
            'id', 'categoryName', 'categoryImg'
        )
    )
    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })


# -------------------- PRODUCT BY CATEGORY --------------------
def product_by_category(request, category_id):
    data = list(
        Product.objects.filter(
            category__id=category_id
        ).values(
            'id',
            'title',
            'price',
            'discount_price',
            'image',
            'remark',
            'star'
        )
    )

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })


# -------------------- PRODUCT BY REMARK --------------------
def product_by_remark(request, remark):
    data = list(
        Product.objects.filter(
            remark=remark
        ).values(
            'id',
            'title',
            'price',
            'discount_price',
            'image',
            'remark',
            'star'
        )
    )

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })


# -------------------- PRODUCT SLIDER --------------------
def product_slider_list(request):
    data = list(
        ProductSlider.objects.values(
            'id',
            'title',
            'short_des',
            'price',
            'image'
        )
    )

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })


# -------------------- PRODUCT SEARCH --------------------
def product_by_keyword(request):
    keyword = request.GET.get('keyword', '')

    data = list(
        Product.objects.filter(
            title__icontains=keyword
        ).values(
            'id',
            'title',
            'price',
            'discount_price',
            'image',
            'remark',
            'star'
        )
    )

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })


# -------------------- PRODUCT DETAILS --------------------
def product_details(request, product_id):
    try:
        # Fetch product data
        product = Product.objects.values(
            'id',
            'title',
            'price',
            'discount_price',
            'image',
            'remark',
            'star'
        ).get(id=product_id)

        # Fetch all product details
        details = list(ProductDetail.objects.filter(product__id=product_id).values(
            'img1',
            'img2',
            'img3',
            'img4',
            'des',
            'color',
            'size'
        ))

        data = {
            'product': product,
            'details': details
        }

        return JsonResponse({
            'status': True,
            'message': 'success',
            'data': data
        })

    except Product.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Product not found',
            'data': None
        })




# -------------------- PRODUCT BY BRAND --------------------
def product_by_brand(request, brand_id):
    data = list(
        Product.objects.filter(
            brand__id=brand_id
        ).values(
            'id',
            'title',
            'price',
            'discount_price',
            'image',
            'remark',
            'star'
        )
    )

    return JsonResponse({
        'status': True,
        'message': 'success',
        'data': data
    })



#Login
@csrf_exempt
def user_login(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()

    if not email:
        return JsonResponse({'status': False, 'message': 'Email is required'}, status=400)

    characters = string.ascii_lowercase + '123456789'
    otp = ''.join(random.choice(characters) for _ in range(5))

    user,created = User.objects.get_or_create(email=email, defaults={'otp': otp})

    if not created:
        user.otp = otp
        user.save()

    return JsonResponse({'status': True, 'message': f"{otp} OTP sent Successfully"}, status=200)


@csrf_exempt
def varify_otp(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    otp = data.get('otp', '').strip()

    if not email or not otp:
        return JsonResponse({'status': False, 'message': 'Email or OTP is required'}, status=400)

    try:
        user = User.objects.get(email=email, otp=otp)

    except User.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'User not found'}, status=400)

    payload = {
        'user_id': user.id,
        'user_email': user.email,
        'exp':datetime.now(timezone.utc) + timedelta(days=30),
        'iat':datetime.now(timezone.utc),
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return JsonResponse({
        'status': True,
        'message': 'success',
        'token': token,
        'data': {'user_id': user.id, 'user_email': user.email}
    })

