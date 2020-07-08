from django.urls import path

from AVShop import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='all_products'),
    path('delete/<int:pk>', views.ProductDelete.as_view(), name='product_delete'),
    path('create/', views.ProductCreate.as_view(), name='new_product'),
    path('edit/<int:pk>', views.ProductUpdate.as_view(), name='edit_product'),
    path('about_us', views.ProtectedTemplateView.as_view(template_name='AVShop/about.html'), name='about_us'),
    # path('<int:product_id>/like/', views.like_product, name='like_product'),
    path('<int:product_id>', views.product_by_id, name='product_by_id'),
    path('<slug:product_name>', views.product_by_name, name='product_by_name'),
    path('search/', views.search, name='products_search'),
]
