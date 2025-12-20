from django.shortcuts import render


def index(request):
    return render(request,'index.html')


def brand_list(request):
    pass


def category_list(request):
    pass


def product_by_category(request, category_id):
    pass


def product_by_remark(request, remark):
    pass


def product_slider_list(request):
    pass


def product_by_keyword(request):
    pass


def product_details(request, product_id):
    pass


def product_by_brand(request, brand):
    pass