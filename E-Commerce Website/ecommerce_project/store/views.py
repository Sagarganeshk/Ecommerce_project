from django.shortcuts import get_object_or_404, redirect, render
from .models import Product
from django.db.models import Value
# Create your views here.

def store_home(request):
    category = request.GET.get('category')  # ?category=Shampoo

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('store_home')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price*quantity
        cart_items.append({
            'product' : product,
            'quantity' : quantity,
            'subtotal' : subtotal
        })
        total += subtotal

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart  = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

def checkout(request):
    total_paid = 0

    cart = request.session.get('cart', {})
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total_paid += product.price * quantity

    # Clear the cart
    if 'cart' in request.session:
        del request.session['cart']

    return render(request, 'store/checkout.html', {'total_paid': total_paid})
  

def update_quantity(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity:
            quantity = int(quantity)
            cart = request.session.get('cart', {})
            cart[str(product_id)] = quantity
            request.session['cart'] = cart
    return redirect('view_cart')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})