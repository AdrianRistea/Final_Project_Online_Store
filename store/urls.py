from django.urls import path
from store import views

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home_page'),
    path('', views.HomeTemplateView.as_view(), name='base'),
    path('login', views.HomeTemplateView.as_view(), name='login'),
    path('create_user/', views.UserCreateView.as_view(), name='create-user'),
    path('product_list/', views.ProductListView.as_view(), name='product_list'),
    path('category/<int:pk>', views.CategoryDetailsView.as_view(), name='category_list'),
    path('product_detail/<int:product_id>/', views.product_details, name='product-detail'),
    path('contact/', views.contact, name='contact'),
    path('create_product/', views.ProductCreateView.as_view(), name="create-product"),
    path('modify_product/<int:pk>/', views.ProductUpdateView.as_view(), name="modify-product"),
    path('delete_product/<int:product_id>/', views.delete_product, name="delete-product"),
    path('open-cart/', views.open_cart_view, name='open_cart'),
    path('add-product-to-cart/', views.add_product_to_cart, name='add_product_to_cart'),
    path('remove-product-from-cart/<int:id>', views.remove_from_cart, name="remove-product-from-cart"),
    path('favorite/', views.remove_from_cart, name="favorite"),

]
