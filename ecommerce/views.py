from django.http import JsonResponse
from django.shortcuts import render
from .models import (
Brand,
Category,
Product,
ProductSlider,
ProductDetail
)

def index(request):
    return render(request,'index.html')


def brand_list(request):
    data = list(Brand.objects.values('id','brandName', 'brandImg'))
    return JsonResponse({'status':True, 'message':'success', 'data':data})


def category_list(request):
    data = list(Category.objects.values('id', 'categoryName', 'categoryImg'))
    return JsonResponse({'status': True, 'message': 'success', 'data': data})


def product_by_category(request, category_id):
    data = list(Product.objects.filter(categoryId=category_id).values(
        'id', 'title', 'price', 'discount_price', 'image', 'remark', 'star'
    ))
    return JsonResponse({'status': True, 'message': 'success', 'data': data})


def product_by_remark(request, remark):
    data = list(Product.objects.filter(remark=remark).values(
        'id', 'title', 'price', 'discount_price', 'image', 'remark', 'star'
    ))
    return JsonResponse({'status': True, 'message': 'success', 'data': data})


def product_slider_list(request):
    pass


def product_by_keyword(request):
    pass


def product_details(request, product_id):
    pass


def product_by_brand(request, brand):
    data = list(Product.objects.filter(brandId=brand).values(
        'id', 'title', 'price', 'discount_price', 'image', 'remark', 'star'
    ))
    return JsonResponse({'status': True, 'message': 'success', 'data': data})
