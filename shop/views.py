from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, CartItem


def home(request):
    return render(request, 'home.html')

def catalog(request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})
def add_to_cart(request, product_id):
    qty = int(request.GET.get('qty', 1))
    product = Product.objects.get(id=product_id)

    item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:
        item.quantity = qty
    else:
        item.quantity += qty

    item.save()
    return redirect('cart')

def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(i.product.price * i.quantity for i in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart')
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import CartItem, Order, OrderItem

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'profile.html', {'orders': orders})
from django.db import transaction
from django.contrib.auth.decorators import login_required

@login_required
@transaction.atomic
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items.exists():
        return redirect('cart')

    total = sum(i.product.price * i.quantity for i in items)

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        status='Новый'
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    items.delete()


    return render(request, 'checkout_success.html', {'order': order})
def about(request):
    return render(request, 'about.html')

def delivery(request):
    return render(request, 'delivery.html')

def contacts(request):
    return render(request, 'contacts.html')

def catalog(request):
    products = Product.objects.all()

    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)

    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'name_asc':
        products = products.order_by('name')
    elif sort == 'name_desc':
        products = products.order_by('-name')

    return render(request, 'catalog.html', {'products': products})
