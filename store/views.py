from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .filters import ProductFilters
from .models import Product, Category, Cart, CartItem
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from store.forms import UserForm, ContactForm, ProductForm, ProductUpdateForm, CheckoutForm, CategoryForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import date

class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    success_message = 'Felicitate! {f_name} {l_name} a fost adaugat cu success!'
    # permission_required = 'student.add_student'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=self.object.name)


class ProductListView(ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = 'all_products'
    fields = '__all__'

    def get_queryset(self):
        return Product.objects.filter(active=True)

    def get_context_data(self, get_all_products=None, **kwargs):
        context = super().get_context_data(**kwargs)

        my_filters = ProductFilters(self.request.GET, queryset=Product.objects.filter(active=True))
        get_all_products = my_filters.qs
        #
        context['products'] = get_all_products
        context['form_filters'] = my_filters.form

        return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def contact_confirm_view(request):
    context = {

        'messages': messages.get_messages(request),
    }
    return render(request, 'success_mail_contact.html', context)


class HomeTemplateView(TemplateView):
    template_name = 'homepage.html'


class UserCreateView(CreateView):
    template_name = 'create_user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')


class CategoryProductsView(DetailView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context['subcategories'] = category.subcategories()
        context['products'] = Product.objects.filter(category=category) | Product.objects.filter(category__in=category.subcategories())
        return context


class ProductUpdateView(UpdateView):
    template_name = 'product_modify.html'
    model = Product
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_list')


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html', {'product': product})

def get(self, request, *args, **kwargs):
    return HttpResponse()

def product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def reduced_products(request):
    reduced_products = Product.objects.filter(discount_price__isnull=False, discount_price_valid_until__gte=date.today())
    return render(request, 'reduced_products.html', {'reduced_products': reduced_products})


@login_required
def add_product_to_cart(request):
    if request.method == 'POST':
        open_cart, created = Cart.objects.get_or_create(user=request.user, status='open')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Verifică dacă produsul există deja în coș și actualizează cantitatea
        cart_item, created = CartItem.objects.get_or_create(product_id=product_id, cart=open_cart)
        cart_item.quantity += quantity
        cart_item.save()

        # Calculează valoarea totală a coșului
        total_value = 0
        product_quantity_map = {}  # Mapare cantitate produs ID
        for item in open_cart.cartitem_set.all():
            if item.product_id in product_quantity_map:
                product_quantity_map[item.product_id] += item.quantity
            else:
                product_quantity_map[item.product_id] = item.quantity

        for product_id, quantity in product_quantity_map.items():
            product = Product.objects.get(pk=product_id)  # Înlocuiește 'Product' cu modelul tău real
            total_value += product.price * quantity

        # Actualizează valoarea totală în obiectul coșului
        open_cart.total_value = total_value
        open_cart.save()

    return redirect(request.META['HTTP_REFERER'])

@login_required()
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, status='open')
    else:
        cart, created = Cart.objects.get_or_create(user=None, status='open', session_key=request.session.session_key)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()

    return redirect('open_cart')



@login_required
def open_cart_view(request):
    open_cart, created = Cart.objects.get_or_create(user=request.user, status='open')
    total_value = 0
    for item in open_cart.cartitem_set.all():
        total_value += item.product.price * item.quantity

    context = {
        'cart': open_cart,
        'total_value': total_value,
    }
    return render(request, 'open_cart.html', context)

def search_results(request):
    query = request.GET.get('query')
    results = []

    if query:
        results = Product.objects.filter(name__icontains=query)  # Schimbă asta cu filtrul tău

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search_results.html', context)

def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            return redirect('home_page')
    else:
        form = CheckoutForm()

    context = {
        'form': form,
    }
    return render(request, 'checkout.html', context)

def proceed_to_payment(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart.cartitem_set.all().delete()
    messages.success(request, "Plata a fost realizată cu succes!")

    return redirect(reverse('home_page'))


class CategoryCreateView(CreateView):
    template_name = 'add_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('home_page')
    success_message = 'Felicitări! Categoria "{name}" a fost adăugată cu succes!'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(name=self.object.name)



