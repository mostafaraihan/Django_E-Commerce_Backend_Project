from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path("brands/", views.brand_list),
    path("categories/", views.category_list),
    path("products/category/<int:category_id>/", views.product_by_category),
    path("products/remark/<str:remark>/", views.product_by_remark),
    path("products/brand/<int:brand_id>/", views.product_by_brand),
    path("products/sliders/", views.product_slider_list),
    path("products/search/", views.product_by_keyword),
    path("products/<int:product_id>/", views.product_details),

    # Authentication endpoints
    path("login/", views.user_login),
    path("verify-otp/", views.verify_otp),

    # Cart endpoints
    path("cart/add/", views.cart_add),
    path("cart/remove/<int:cart_id>/", views.cart_remove),
    path("cart/list/", views.cart_list),

    # Wishlist endpoints
    path("wish/add/", views.wish_add),
    path("wish/remove/<int:wish_id>/", views.wish_remove),
    path("wish/list/", views.wish_list),

    # Invoice endpoints
    path("invoice/create/", views.create_invoice),
    path("invoice/list/", views.invoice_list),
]
