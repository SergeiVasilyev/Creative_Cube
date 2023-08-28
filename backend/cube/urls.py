"""
URL configuration for cube_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path, re_path
from shop.views import *
from shop import views
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'products', ProductsViewSet, basename='products') # basename - need if we don't use in Post_articleViewSet queryset variable

# print(router.urls)
# router2 = routers.SimpleRouter()
# router2.register(r'posts', Post_articleAPIView2)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name="main"),
    path('products/', products, name="products"),
    path('product/<slug>/', product, name="product"),
    path('cart/', CartView.as_view(), name="cart"),
    path('add_to_cart/<int:idx>/', AddToCartView.as_view(), name="add_to_cart"),
    path('clear_cart/', clear_cart, name="clear_cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),

    # Django AUTHENTICATION URLS (LOGIN, REGISTER, LOGOUT)
    path('login/', LoginView.as_view(), name="login_view"),
    path('register/', RegisterView.as_view(), name="register_view"),
    path('logout/', LogoutView.as_view(), name="logout_view"),

    path('sucsess/', sucsess, name="sucsess"),
    path('payment/', payment, name="payment"),
    path('payment2/', payment2, name="payment2"),
    path('capture/<str:orderID>', capture, name="capture"),
    path('ok/', ok, name="ok"),
    path('not_ok/', not_ok, name="not_ok"),
    path('orders/', orders, name="orders"),
    path('sucsess_payment/<str:orderID>', sucsess_payment, name="sucsess_payment"),

    path('create_product/', create_product, name="create_product"),
    
    path('404/', page_not_found, name="404"),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gallery/', gallery, name="gallery"),

    # DJOSER AUTHENTICATION URLS (LOGIN, REGISTER, LOGOUT)
    re_path(r'^api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/', include('djoser.urls.authtoken')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
