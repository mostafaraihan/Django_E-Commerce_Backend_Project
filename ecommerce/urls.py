from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('brands/', views.brand_list),
    path('categories/', views.category_list),

    path('products/category/<int:category_id>/', views.product_by_category),
    path('products/remark/<str:remark>/', views.product_by_remark),
    path('products/brand/<int:brand_id>/', views.product_by_brand),

    path('products/sliders/', views.product_slider_list),
    path('products/search/', views.product_by_keyword),

    path('products/<int:product_id>/', views.product_details),
]