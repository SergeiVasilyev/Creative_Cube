import requests
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import (
    HttpResponse,
    JsonResponse,
)
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, Group 
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# from .serializers import UserSerializer, GroupSerializer

from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from .models import ShoppingSession, Product, Order, OrderItem
from .services import *
from .authentication import *
from django.db.models import Avg, Count, Min, Sum, F
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .payment import *
from .get_token import get_token
from .make_paypal_data_request import *

from dotenv import load_dotenv
from pathlib import Path

from .api import *


dotenv_path = Path('../Backend/.env')
load_dotenv(dotenv_path=dotenv_path)



def create_shopping_session(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Create a new session for the authenticated user
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    shopping_session = ShoppingSession.objects.create(session_key=session_key, user=request.user)
    return redirect('home')


def main(request):
    print(request.session.session_key)
    print(os.getenv('PAYPAL_URL'))
    return render(request, 'main.html')


def page_not_found(request):
    return render(request, '404.html')


def products(request):
    products = Product.objects.filter(availability=True).order_by('id')

    context = {
        'products': products
    }
    return render(request, 'products.html', context)


def product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product
    }
    return render(request, 'product.html', context)



class AddToCartView(View):
    template_name = 'cart'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, idx):
        product_id = str(idx)
        quantity = request.GET.get('quantity', 1)
        
        product = get_object_or_404(Product, id=product_id)

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] += int(quantity)
        else:
            cart[product_id] = {'quantity': int(quantity), 'price': str(product.price)}

        request.session['cart'] = cart

        messages.success(request, f"{quantity} {product.name}(s) added to cart.")
        return redirect(self.template_name)


class CartView(View):
    template_name = 'cart.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        cart = request.session.get('cart', {})
        print('view', request.session.get('cart', {}))
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        print(product_ids)

        cart_items = []
        total_price = 0
        for product in products:
            cart_item = {
                'product': product,
                'quantity': cart[str(product.id)]['quantity'],
                'subtotal': float(product.price) * int(cart[str(product.id)]['quantity'])
            }
            total_price += cart_item['subtotal']
            cart_items.append(cart_item)

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }

        return render(request, self.template_name, context)
    
    @method_decorator(login_required(login_url='/login/'))
    def post(self, request):
        session = Session.objects.get(session_key=request.session.session_key)
        cart = request.session.get('cart', {})
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        order, order_created = Order.objects.get_or_create(customer=request.user, session=session, complete=False)
        order_items = []
        ThroughModel = Order.items.through
        for product in products:
            order_item, order_item_created = OrderItem.objects.get_or_create(product=product, customer=request.user, session=session)
            if not order_item_created:
                order_item.quantity=order_item.quantity+1
                order_item.save()
            else:
                order_item.quantity=cart[str(product.id)]['quantity']
                order_item.save()
                order_items.append(ThroughModel(order_id=order.id, orderitem_id=order_item.id))
        order.items.through.objects.bulk_create(order_items)
        # https://www.reddit.com/r/django/comments/4fxp92/how_do_i_use_bulk_create_when_model_has_m2m_field/

        request.session['cart'] = {}

        messages.success(request, 'Order placed successfully!')
        # return render(request, self.template_name)
        return redirect('checkout')
    



def clear_cart(request):
    request.session['cart'] = {}

    return redirect('cart')


class CheckoutView(View):
    template_name = 'checkout.html'

    @method_decorator(login_required(login_url='/login/'))
    def get(self, request):
        try:
            order = Order.objects.get(customer=request.user, complete=False)
        except:
            return redirect('cart')
        
        items = order.items.all().order_by('-date_added')
        total_price = items.annotate(total=F('product__price') * F('quantity')).aggregate(sum=Sum('total'))

        context = {
            'items': items,
            'total_price': total_price,
        }
        return render(request, self.template_name, context)




def sucsess(request):
    return HttpResponse('SUCSESS')



# https://github.com/paypal-examples/docs-examples/blob/main/standard-integration/paypal-api.js
# https://developer.paypal.com/demo/checkout/#/pattern/server

# @csrf_exempt
def payment(request):
    token = get_token()
    if request.method == 'POST':
        get_ordered_items = Order.objects.get(customer=request.user, complete=False)
        paypal_data_request = create_paypal_data_request(get_ordered_items)
        response = paypal_pay(token, paypal_data_request)
        # print(response.json(), sep="\n")

    return JsonResponse(response.json())


# @csrf_exempt
def capture(request, orderID):
    order_res = json.load(request)
    order_detail = paypal_checkout_orders(orderID)

    response = paypal_capture(orderID)
    ordered_items = Order.objects.get(customer=request.user, complete=False)
    ordered_items.complete = True
    ordered_items.session = None
    ordered_items.transaction_id = orderID
    ordered_items.items.all().update(session=None)
    ordered_items.save()
   
    return JsonResponse(response.json())


def sucsess_payment(request, orderID):
    order = Order.objects.get(transaction_id=orderID)
    print(order)
    try:
        order = Order.objects.get(transaction_id=orderID)
    except:
        messages.error(request, f"Order not found")
    return render(request, 'sucsess_payment.html', {'order': order})


def payment2(request):
    return render(request, 'payment2.html')


def ok(request):
    print(request.POST)
    # print(json.load(request)['post_data'])
    # orderID = json.load(request)['orderID']

    token = get_token()
    response = paypal_checkout_orders('9TM244411J853740K')
    print(response.json()['id'])
    print(str(response.json()))

    get_ordered_items = Order.objects.get(customer=request.user, transaction_id=response.json()['id'], complete=True)
    get_ordered_items.response_data = str(response.json())
    get_ordered_items.save()
    return HttpResponse('PAYMENT SUCSESS')


def not_ok():
    return HttpResponse('PAYMENT REJECTED')


def orders(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {'orders': orders})


def create_product(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        product_name = request.POST.get('p_name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        slug = create_slug(product_name)
        date_added = datetime_now()

        product = Product.objects.create(name=product_name,
                                         description=description,
                                         price=price,
                                         quantity=quantity,
                                         slug=slug, 
                                         date_added=date_added)
        for image in images:
            product.images.create(img_name=image)

    products = Product.objects.all()
    return render(request, 'create_product.html', {'products': products})


def gallery(request):
    return render(request, 'gallery.html')


