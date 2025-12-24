from django.http import JsonResponse
from django.shortcuts import render
from .models import (
    Brand,
    Category,
    Product,
    ProductSlider,
    ProductDetail
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
        product = Product.objects.values(
            'id',
            'title',
            'price',
            'discount_price',
            'image',
            'remark',
            'star'
        ).get(id=product_id)

        details = ProductDetail.objects.values(
            'img1',
            'img2',
            'img3',
            'img4',
            'des',
            'color',
            'size'
        ).get(product__id=product_id)

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

    except ProductDetail.DoesNotExist:
        return JsonResponse({
            'status': False,
            'message': 'Product details not found',
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
